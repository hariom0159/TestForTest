// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PaymentGateway {

    struct Loan {
        uint256 loanId;
        address borrower;
        uint256 amount;
        bool isRepaid;
    }

    mapping(uint256 => Loan) public loans;
    uint256 public nextLoanId;

    event LoanIssued(uint256 loanId, address borrower, uint256 amount);
    event LoanRepaid(uint256 loanId, address borrower, uint256 amount);

    // Issue a loan
    function issueLoan(address _borrower, uint256 _amount) public {
        require(_amount > 0, "Loan amount must be greater than 0");

        loans[nextLoanId] = Loan(nextLoanId, _borrower, _amount, false);
        
        emit LoanIssued(nextLoanId, _borrower, _amount);
        nextLoanId++;
    }

    // Repay a loan
    function repayLoan(uint256 _loanId) public payable {
        Loan storage loan = loans[_loanId];

        require(loan.borrower == msg.sender, "Not the loan owner");
        require(!loan.isRepaid, "Loan already repaid");
        require(msg.value >= loan.amount, "Insufficient repayment amount");

        loan.isRepaid = true;
        
        emit LoanRepaid(_loanId, msg.sender, msg.value);
    }

    // Check loan details
    function getLoan(uint256 _loanId) public view returns (
        uint256, address, uint256, bool
    ) {
        Loan memory loan = loans[_loanId];
        return (
            loan.loanId,
            loan.borrower,
            loan.amount,
            loan.isRepaid
        );
    }
}
