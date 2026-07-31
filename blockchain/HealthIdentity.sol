// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title HealthIdentity
 * @dev Quantum-Secured Digital Health Identity Smart Contract.
 * Manages Role-Based Access Control (RBAC) and off-chain EHR hashes.
 */
contract HealthIdentity {
    
    address public admin;

    struct Patient {
        string aadhaarHash; // Pseudonymous identifier
        string pqcPublicKey; // Post-Quantum public key for securing data
        string ehrIpfsHash; // Off-chain encrypted health record pointer
        bool isRegistered;
    }

    // Mappings
    mapping(address => Patient) public patients;
    mapping(address => bool) public authorizedDoctors;
    mapping(address => mapping(address => bool)) public doctorAccess; // Patient -> Doctor -> Access

    // Events for Audit Logging (Mitigates Repudiation)
    event PatientRegistered(address indexed patientAddress, string aadhaarHash);
    event EHRUpdated(address indexed patientAddress, string newEhrIpfsHash);
    event AccessGranted(address indexed patientAddress, address indexed doctorAddress);
    event AccessRevoked(address indexed patientAddress, address indexed doctorAddress);
    event DoctorAuthorized(address indexed doctorAddress);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Not authorized: Admin only");
        _;
    }

    modifier onlyRegisteredPatient() {
        require(patients[msg.sender].isRegistered, "Not authorized: Patient not registered");
        _;
    }

    modifier onlyAuthorizedDoctor() {
        require(authorizedDoctors[msg.sender], "Not authorized: Doctor not registered");
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    /**
     * @dev Admin authorizes a medical professional
     */
    function authorizeDoctor(address _doctor) external onlyAdmin {
        authorizedDoctors[_doctor] = true;
        emit DoctorAuthorized(_doctor);
    }

    /**
     * @dev Register a new patient in the system
     */
    function registerPatient(string memory _aadhaarHash, string memory _pqcPublicKey) external {
        require(!patients[msg.sender].isRegistered, "Patient already registered");
        
        patients[msg.sender] = Patient({
            aadhaarHash: _aadhaarHash,
            pqcPublicKey: _pqcPublicKey,
            ehrIpfsHash: "",
            isRegistered: true
        });

        emit PatientRegistered(msg.sender, _aadhaarHash);
    }

    /**
     * @dev Patient grants access to a specific doctor
     */
    function grantAccess(address _doctor) external onlyRegisteredPatient {
        require(authorizedDoctors[_doctor], "Doctor is not authorized by the network");
        doctorAccess[msg.sender][_doctor] = true;
        emit AccessGranted(msg.sender, _doctor);
    }

    /**
     * @dev Patient revokes access from a specific doctor
     */
    function revokeAccess(address _doctor) external onlyRegisteredPatient {
        doctorAccess[msg.sender][_doctor] = false;
        emit AccessRevoked(msg.sender, _doctor);
    }

    /**
     * @dev Doctor updates the patient's EHR hash (e.g., after a new diagnosis)
     */
    function updateEHR(address _patient, string memory _newEhrIpfsHash) external onlyAuthorizedDoctor {
        require(doctorAccess[_patient][msg.sender], "Not authorized: Patient has not granted access");
        
        patients[_patient].ehrIpfsHash = _newEhrIpfsHash;
        emit EHRUpdated(_patient, _newEhrIpfsHash);
    }

    /**
     * @dev Retrieve the patient's EHR hash (Can be called by patient or authorized doctor)
     */
    function getEHRHash(address _patient) external view returns (string memory) {
        require(
            msg.sender == _patient || doctorAccess[_patient][msg.sender],
            "Not authorized to view this record"
        );
        return patients[_patient].ehrIpfsHash;
    }
}
