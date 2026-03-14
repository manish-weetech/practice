import { Request, Response } from 'express';
import { StatusCodes } from 'http-status-codes';
import Account from '../models/Account';

// GET /api/accounts
export const getMyAccounts = async (req: Request, res: Response): Promise<void> => {
  try {
    const accounts = await Account.find({ userId: req.user!._id });
    res.status(StatusCodes.OK).json({ success: true, message: 'Success', data: accounts });
  } catch (err) {
    res.status(StatusCodes.INTERNAL_SERVER_ERROR).json({ success: false, message: (err as Error).message });
  }
};

// GET /api/accounts/:id
export const getAccountById = async (req: Request, res: Response): Promise<void> => {
  try {
    const account = await Account.findOne({ _id: req.params.id, userId: req.user!._id });
    if (!account) {
      res.status(StatusCodes.NOT_FOUND).json({ success: false, message: 'Account not found.' });
      return;
    }
    res.status(StatusCodes.OK).json({ success: true, message: 'Success', data: account });
  } catch (err) {
    res.status(StatusCodes.INTERNAL_SERVER_ERROR).json({ success: false, message: (err as Error).message });
  }
};

// PATCH /api/accounts/:id/toggle
export const toggleAccountStatus = async (req: Request, res: Response): Promise<void> => {
  try {
    const account = await Account.findOne({ _id: req.params.id, userId: req.user!._id });
    if (!account) {
      res.status(StatusCodes.NOT_FOUND).json({ success: false, message: 'Account not found.' });
      return;
    }

    account.isActive = !account.isActive;
    await account.save();

    res.status(StatusCodes.OK).json({
      success: true,
      message: `Account ${account.isActive ? 'activated' : 'deactivated'} successfully`,
      data: account,
    });
  } catch (err) {
    res.status(StatusCodes.INTERNAL_SERVER_ERROR).json({ success: false, message: (err as Error).message });
  }
};
