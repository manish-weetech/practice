import { z } from 'zod';

const objectId = z
  .string()
  .regex(/^[a-f\d]{24}$/i, 'Must be a valid MongoDB ObjectId');

export const depositSchema = z.object({
  accountId:   objectId,
  amount:      z.number().positive('Amount must be positive'),
  description: z.string().trim().max(200).optional(),
});

export const withdrawSchema = z.object({
  accountId:   objectId,
  amount:      z.number().positive('Amount must be positive'),
  description: z.string().trim().max(200).optional(),
});

export const transferSchema = z.object({
  fromAccountId: objectId,
  toAccountId:   objectId,
  amount:        z.number().positive('Amount must be positive'),
  description:   z.string().trim().max(200).optional(),
});

export type DepositInput   = z.infer<typeof depositSchema>;
export type WithdrawInput  = z.infer<typeof withdrawSchema>;
export type TransferInput  = z.infer<typeof transferSchema>;
