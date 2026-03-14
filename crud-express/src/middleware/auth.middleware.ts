import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { StatusCodes } from 'http-status-codes';
import { JWT_SECRET } from '../config/env';
import User from '../models/User';

export const protect = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
  try {
    const authHeader = req.headers.authorization;

    if (!authHeader?.startsWith('Bearer ')) {
      res.status(StatusCodes.UNAUTHORIZED).json({ success: false, message: 'Access denied. No token provided.' });
      return;
    }

    const token = authHeader.split(' ')[1];
    const decoded = jwt.verify(token, JWT_SECRET) as { id: string };

    const user = await User.findById(decoded.id);
    if (!user) {
      res.status(StatusCodes.UNAUTHORIZED).json({ success: false, message: 'User belonging to this token no longer exists.' });
      return;
    }

    req.user = user;
    next();
  } catch (error) {
    if (error instanceof jwt.TokenExpiredError) {
      res.status(StatusCodes.UNAUTHORIZED).json({ success: false, message: 'Token expired. Please log in again.' });
      return;
    }
    if (error instanceof jwt.JsonWebTokenError) {
      res.status(StatusCodes.UNAUTHORIZED).json({ success: false, message: 'Invalid token.' });
      return;
    }
    next(error);
  }
};
