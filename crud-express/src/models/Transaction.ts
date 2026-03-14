import mongoose, { Document, Schema, Types } from 'mongoose';

export type TransactionType = 'DEPOSIT' | 'WITHDRAWAL' | 'TRANSFER';
export type TransactionStatus = 'PENDING' | 'COMPLETED' | 'FAILED';

export interface ITransaction extends Document {
  fromAccount?: Types.ObjectId;
  toAccount?: Types.ObjectId;
  amount: number;
  type: TransactionType;
  status: TransactionStatus;
  description: string;
  balanceAfter: number | null;
  createdAt: Date;
  updatedAt: Date;
}

const transactionSchema = new Schema<ITransaction>(
  {
    fromAccount: { type: Schema.Types.ObjectId, ref: 'Account', default: null },
    toAccount:   { type: Schema.Types.ObjectId, ref: 'Account', default: null },
    amount: {
      type: Number,
      required: [true, 'Amount is required'],
      min: [0.01, 'Amount must be at least 0.01'],
    },
    type: {
      type: String,
      enum: ['DEPOSIT', 'WITHDRAWAL', 'TRANSFER'] satisfies TransactionType[],
      required: true,
    },
    status: {
      type: String,
      enum: ['PENDING', 'COMPLETED', 'FAILED'] satisfies TransactionStatus[],
      default: 'PENDING',
    },
    description: { type: String, trim: true, default: '' },
    balanceAfter: { type: Number, default: null },
  },
  { timestamps: true }
);

export default mongoose.model<ITransaction>('Transaction', transactionSchema);
