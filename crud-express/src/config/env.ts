import 'dotenv/config';

const _required = (key: string): string => {
  const val = process.env[key];
  if (!val) throw new Error(`Missing required env variable: ${key}`);
  return val;
};

export const PORT: number = Number(process.env.PORT) || 3000;
export const MONGO_URI: string = _required('MONGO_URI');
export const JWT_SECRET: string = _required('JWT_SECRET');
export const JWT_EXPIRES_IN: string = process.env.JWT_EXPIRES_IN ?? '7d';
export const NODE_ENV: string = process.env.NODE_ENV ?? 'development';
