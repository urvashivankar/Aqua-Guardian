// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title PollutionRegistry
 * @dev Smart contract for storing pollution report hashes on-chain
 * @notice This contract provides an immutable audit trail for water pollution reports
 */
contract PollutionRegistry {
    
    // ========================================================================
    // STATE VARIABLES
    // ========================================================================
    
    address public owner;
    uint256 public reportCount;
    
    struct Report {
        bytes32 reportHash;      // SHA-256 hash of report data
        uint256 timestamp;       // Block timestamp
        address submitter;       // Address that submitted the hash
        bool verified;           // Verification status
    }
    
    // Mapping from report ID to Report struct
    mapping(uint256 => Report) public reports;
    
    // Mapping from report hash to report ID (prevent duplicates)
    mapping(bytes32 => uint256) public hashToReportId;
    
    // ========================================================================
    // EVENTS
    // ========================================================================
    
    event ReportLogged(
        uint256 indexed reportId,
        bytes32 indexed reportHash,
        address indexed submitter,
        uint256 timestamp
    );
    
    event ReportVerified(
        uint256 indexed reportId,
        address indexed verifier,
        uint256 timestamp
    );
    
    event OwnershipTransferred(
        address indexed previousOwner,
        address indexed newOwner
    );
    
    // ========================================================================
    // MODIFIERS
    // ========================================================================
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    modifier reportExists(uint256 _reportId) {
        require(_reportId > 0 && _reportId <= reportCount, "Report does not exist");
        _;
    }
    
    // ========================================================================
    // CONSTRUCTOR
    // ========================================================================
    
    constructor() {
        owner = msg.sender;
        reportCount = 0;
    }
    
    // ========================================================================
    // PUBLIC FUNCTIONS
    // ========================================================================
    
    /**
     * @dev Log a new pollution report hash
     * @param _reportHash SHA-256 hash of the report data
     * @return reportId The ID of the newly logged report
     */
    function logReport(bytes32 _reportHash) public onlyOwner returns (uint256) {
        require(_reportHash != bytes32(0), "Invalid report hash");
        require(hashToReportId[_reportHash] == 0, "Report hash already exists");
        
        reportCount++;
        uint256 newReportId = reportCount;
        
        reports[newReportId] = Report({
            reportHash: _reportHash,
            timestamp: block.timestamp,
            submitter: msg.sender,
            verified: false
        });
        
        hashToReportId[_reportHash] = newReportId;
        
        emit ReportLogged(newReportId, _reportHash, msg.sender, block.timestamp);
        
        return newReportId;
    }
    
    /**
     * @dev Verify a pollution report (admin/NGO action)
     * @param _reportId The ID of the report to verify
     */
    function verifyReport(uint256 _reportId) public onlyOwner reportExists(_reportId) {
        require(!reports[_reportId].verified, "Report already verified");
        
        reports[_reportId].verified = true;
        
        emit ReportVerified(_reportId, msg.sender, block.timestamp);
    }
    
    /**
     * @dev Get report details by ID
     * @param _reportId The ID of the report
     * @return reportHash The hash of the report
     * @return timestamp When the report was logged
     * @return submitter Who submitted the report
     * @return verified Whether the report has been verified
     */
    function getReport(uint256 _reportId) 
        public 
        view 
        reportExists(_reportId) 
        returns (
            bytes32 reportHash,
            uint256 timestamp,
            address submitter,
            bool verified
        ) 
    {
        Report memory report = reports[_reportId];
        return (
            report.reportHash,
            report.timestamp,
            report.submitter,
            report.verified
        );
    }
    
    /**
     * @dev Check if a report hash exists
     * @param _reportHash The hash to check
     * @return exists Whether the hash exists
     * @return reportId The ID of the report (0 if not exists)
     */
    function reportHashExists(bytes32 _reportHash) 
        public 
        view 
        returns (bool exists, uint256 reportId) 
    {
        reportId = hashToReportId[_reportHash];
        exists = reportId != 0;
        return (exists, reportId);
    }
    
    /**
     * @dev Get total number of reports
     * @return Total reports logged
     */
    function getTotalReports() public view returns (uint256) {
        return reportCount;
    }
    
    /**
     * @dev Transfer ownership
     * @param newOwner Address of the new owner
     */
    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0), "New owner cannot be zero address");
        address previousOwner = owner;
        owner = newOwner;
        emit OwnershipTransferred(previousOwner, newOwner);
    }
}
