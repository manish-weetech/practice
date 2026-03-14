import { Request, Response, NextFunction } from 'express';
import { StatusCodes } from 'http-status-codes';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const errorHandler = (err: Error, _req: Request, res: Response, _next: NextFunction): void => {
  console.error('[ERROR]', err.message);
  res.status(StatusCodes.INTERNAL_SERVER_ERROR).json({ success: false, message: err.message || 'Internal Server Error' });
};
