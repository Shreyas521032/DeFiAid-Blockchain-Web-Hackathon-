// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TransactionStorage {
    struct Transaction {
        bytes32 transactionId;
        uint256 amount;
        bytes32 currency;
        bytes32 debtor;
        bytes32 creditor;
        bytes32 status;
    }

    mapping(bytes32 => Transaction) public transactions;

    event TransactionStored(bytes32 indexed transactionId);

    function storeTransaction(
        bytes32 _transactionId,
        uint256 _amount,
        bytes32 _currency,
        bytes32 _debtor,
        bytes32 _creditor,
        bytes32 _status
    ) public {
        transactions[_transactionId] = Transaction(
            _transactionId,
            _amount,
            _currency,
            _debtor,
            _creditor,
            _status
        );

        emit TransactionStored(_transactionId);
    }

    function getTransaction(bytes32 _transactionId) public view returns (Transaction memory) {
        return transactions[_transactionId];
    }
}
