// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract KYCAMLVerification {

    // Struct to hold customer details
    struct Customer {
        string name;
        string idNumber;
        bool isKYCVerified;
        bool isFlagged; // AML flag
        uint256 riskScore; 
    }

    mapping(address => Customer) public customers;

    address public admin;

    event KYCVerified(address indexed customer, string name, bool status);
    event AMLFlagged(address indexed customer, string reason);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can call this.");
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    // Register customer with initial KYC status
    function registerCustomer(
        address _customer,
        string memory _name,
        string memory _idNumber
    ) public onlyAdmin {
        customers[_customer] = Customer(_name, _idNumber, false, false, 0);
    }

    // Perform KYC verification
    function verifyKYC(address _customer) public onlyAdmin {
        require(bytes(customers[_customer].name).length > 0, "Customer not registered");
        customers[_customer].isKYCVerified = true;
        emit KYCVerified(_customer, customers[_customer].name, true);
    }

    // AML Check - Flag suspicious customers
    function flagSuspiciousActivity(address _customer, uint256 _riskScore) public onlyAdmin {
        require(customers[_customer].isKYCVerified, "Customer must be KYC verified first");

        // Basic AML check: flag if risk score exceeds threshold
        if (_riskScore >= 70) {
            customers[_customer].isFlagged = true;
            emit AMLFlagged(_customer, "Suspicious activity detected");
        }
        
        customers[_customer].riskScore = _riskScore;
    }

    // Retrieve customer details
    function getCustomer(address _customer) public view returns (
        string memory, string memory, bool, bool, uint256
    ) {
        Customer memory customer = customers[_customer];
        return (
            customer.name,
            customer.idNumber,
            customer.isKYCVerified,
            customer.isFlagged,
            customer.riskScore
        );
    }
}
