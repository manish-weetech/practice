import bcrypt from 'bcryptjs';
import { Request, Response } from 'express';
import { StatusCodes } from 'http-status-codes';
import User from '../models/User';
import Account from '../models/Account';
import { signToken } from '../utils/jwt.util';
import { generateAccountNumber } from '../utils/account.util';
import { RegisterInput, LoginInput } from '../validators/auth.validator';

// POST /api/auth/register
export const register = async (req: Request, res: Response): Promise<void> => {
  try {
    const { name, email, password } = req.body as RegisterInput;

    const existingUser = await User.findOne({ email });
    if (existingUser) {
      res.status(StatusCodes.CONFLICT).json({ success: false, message: 'Email already registered.' });
      return;
    }

    const hashedPassword = await bcrypt.hash(password, 12);
    const user = await User.create({ name, email, password: hashedPassword });

    const accountNumber = await generateAccountNumber();
    const account = await Account.create({ userId: user._id, accountNumber });

    const token = signToken({ id: user._id });

    res.status(StatusCodes.CREATED).json({
      success: true,
      message: 'Registration successful',
      data: {
        token,
        user: { id: user._id, name: user.name, email: user.email },
        account: {
          id: account._id,
          accountNumber: account.accountNumber,
          balance: account.balance,
          currency: account.currency,
        },
      },
    });
  } catch (err) {
    res.status(StatusCodes.INTERNAL_SERVER_ERROR).json({ success: false, message: (err as Error).message });
  }
};

// POST /api/auth/login
export const login = async (req: Request, res: Response): Promise<void> => {
  try {
    const { email, password } = req.body as LoginInput;

    const user = await User.findOne({ email }).select('+password');
    if (!user || !(await bcrypt.compare(password, user.password))) {
      res.status(StatusCodes.UNAUTHORIZED).json({ success: false, message: 'Invalid email or password.' });
      return;
    }

    const token = signToken({ id: user._id });

    res.status(StatusCodes.OK).json({
      success: true,
      message: 'Login successful',
      data: { token, user: { id: user._id, name: user.name, email: user.email } },
    });
  } catch (err) {
    res.status(StatusCodes.INTERNAL_SERVER_ERROR).json({ success: false, message: (err as Error).message });
  }
};

// GET /api/auth/me  (protected)
export const getMe = async (req: Request, res: Response): Promise<void> => {
  try {
    const accounts = await Account.find({ userId: req.user!._id });
    res.status(StatusCodes.OK).json({
      success: true,
      message: 'Success',
      data: {
        user: {
          id: req.user!._id,
          name: req.user!.name,
          email: req.user!.email,
          createdAt: req.user!.createdAt,
        },
        accounts,
      },
    });
  } catch (err) {
    res.status(StatusCodes.INTERNAL_SERVER_ERROR).json({ success: false, message: (err as Error).message });
  }
};
