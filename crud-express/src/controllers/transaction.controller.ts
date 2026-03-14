import mongoose from "mongoose";
import { Request, Response } from "express";
import { StatusCodes } from "http-status-codes";
import Account from "../models/Account";
import Transaction from "../models/Transaction";
import {
  DepositInput,
  WithdrawInput,
  TransferInput,
} from "../validators/transaction.validator";

// POST /api/transactions/deposit
export const deposit = async (req: Request, res: Response): Promise<void> => {
  const session = await mongoose.startSession();
  session.startTransaction();

  try {
    const { accountId, amount, description } = req.body as DepositInput;

    const account = await Account.findOne({
      _id: accountId,
      userId: req.user!._id,
    }).session(session);
    if (!account) {
      await session.abortTransaction();
      res
        .status(StatusCodes.NOT_FOUND)
        .json({ success: false, message: "Account not found." });
      return;
    }
    if (!account.isActive) {
      await session.abortTransaction();
      res
        .status(StatusCodes.BAD_REQUEST)
        .json({ success: false, message: "Account is inactive." });
      return;
    }

    account.balance += amount;
    await account.save({ session });

    const [transaction] = await Transaction.create(
      [
        {
          toAccount: account._id,
          amount,
          type: "DEPOSIT",
          status: "COMPLETED",
          description: description ?? "Deposit",
          balanceAfter: account.balance,
        },
      ],
      { session },
    );

    await session.commitTransaction();
    res
      .status(StatusCodes.CREATED)
      .json({
        success: true,
        message: "Deposit successful",
        data: { transaction, newBalance: account.balance },
      });
  } catch (err) {
    await session.abortTransaction();
    res
      .status(StatusCodes.INTERNAL_SERVER_ERROR)
      .json({ success: false, message: (err as Error).message });
  } finally {
    session.endSession();
  }
};

// POST /api/transactions/withdraw
export const withdraw = async (req: Request, res: Response): Promise<void> => {
  const session = await mongoose.startSession();
  session.startTransaction();

  try {
    const { accountId, amount, description } = req.body as WithdrawInput;

    const account = await Account.findOne({
      _id: accountId,
      userId: req.user!._id,
    }).session(session);
    if (!account) {
      await session.abortTransaction();
      res
        .status(StatusCodes.NOT_FOUND)
        .json({ success: false, message: "Account not found." });
      return;
    }
    if (!account.isActive) {
      await session.abortTransaction();
      res
        .status(StatusCodes.BAD_REQUEST)
        .json({ success: false, message: "Account is inactive." });
      return;
    }
    if (account.balance < amount) {
      await session.abortTransaction();
      res
        .status(StatusCodes.BAD_REQUEST)
        .json({ success: false, message: "Insufficient balance." });
      return;
    }

    account.balance -= amount;
    await account.save({ session });

    const [transaction] = await Transaction.create(
      [
        {
          fromAccount: account._id,
          amount,
          type: "WITHDRAWAL",
          status: "COMPLETED",
          description: description ?? "Withdrawal",
          balanceAfter: account.balance,
        },
      ],
      { session },
    );

    await session.commitTransaction();
    res
      .status(StatusCodes.CREATED)
      .json({
        success: true,
        message: "Withdrawal successful",
        data: { transaction, newBalance: account.balance },
      });
  } catch (err) {
    await session.abortTransaction();
    res
      .status(StatusCodes.INTERNAL_SERVER_ERROR)
      .json({ success: false, message: (err as Error).message });
  } finally {
    session.endSession();
  }
};

// POST /api/transactions/transfer
export const transfer = async (req: Request, res: Response): Promise<void> => {
  const session = await mongoose.startSession();
  session.startTransaction();

  try {
    const { fromAccountId, toAccountId, amount, description } =
      req.body as TransferInput;

    if (fromAccountId === toAccountId) {
      await session.abortTransaction();
      res
        .status(StatusCodes.BAD_REQUEST)
        .json({
          success: false,
          message: "Cannot transfer to the same account.",
        });
      return;
    }

    const fromAccount = await Account.findOne({
      _id: fromAccountId,
      userId: req.user!._id,
    }).session(session);
    if (!fromAccount) {
      await session.abortTransaction();
      res
        .status(StatusCodes.NOT_FOUND)
        .json({ success: false, message: "Source account not found." });
      return;
    }
    if (!fromAccount.isActive) {
      await session.abortTransaction();
      res
        .status(StatusCodes.BAD_REQUEST)
        .json({ success: false, message: "Source account is inactive." });
      return;
    }
    if (fromAccount.balance < amount) {
      await session.abortTransaction();
      res
        .status(StatusCodes.BAD_REQUEST)
        .json({ success: false, message: "Insufficient balance." });
      return;
    }

    const toAccount = await Account.findById(toAccountId).session(session);
    if (!toAccount) {
      await session.abortTransaction();
      res
        .status(StatusCodes.NOT_FOUND)
        .json({ success: false, message: "Destination account not found." });
      return;
    }
    if (!toAccount.isActive) {
      await session.abortTransaction();
      res
        .status(StatusCodes.BAD_REQUEST)
        .json({ success: false, message: "Destination account is inactive." });
      return;
    }

    fromAccount.balance -= amount;
    toAccount.balance += amount;
    await fromAccount.save({ session });
    await toAccount.save({ session });

    const [transaction] = await Transaction.create(
      [
        {
          fromAccount: fromAccount._id,
          toAccount: toAccount._id,
          amount,
          type: "TRANSFER",
          status: "COMPLETED",
          description: description ?? "Fund transfer",
          balanceAfter: fromAccount.balance,
        },
      ],
      { session },
    );

    await session.commitTransaction();
    res
      .status(StatusCodes.CREATED)
      .json({
        success: true,
        message: "Transfer successful",
        data: {
          transaction,
          senderNewBalance: fromAccount.balance,
          receiverNewBalance: toAccount.balance,
        },
      });
  } catch (err) {
    await session.abortTransaction();
    res
      .status(StatusCodes.INTERNAL_SERVER_ERROR)
      .json({ success: false, message: (err as Error).message });
  } finally {
    session.endSession();
  }
};

// GET /api/transactions
export const getTransactions = async (
  req: Request,
  res: Response,
): Promise<void> => {
  try {
    const accounts = await Account.find({ userId: req.user!._id }).select(
      "_id",
    );
    const accountIds = accounts.map((a) => a._id);

    const transactions = await Transaction.find({
      $or: [
        { fromAccount: { $in: accountIds } },
        { toAccount: { $in: accountIds } },
      ],
    })
      .populate("fromAccount", "accountNumber currency")
      .populate("toAccount", "accountNumber currency")
      .sort({ createdAt: -1 })
      .limit(50);

    res
      .status(StatusCodes.OK)
      .json({ success: true, message: "Success", data: transactions });
  } catch (err) {
    res
      .status(StatusCodes.INTERNAL_SERVER_ERROR)
      .json({ success: false, message: (err as Error).message });
  }
};
