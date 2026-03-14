import 'dotenv/config';
import app from './app';
import connectDB from './config/db';
import { PORT } from './config/env';

const startServer = async (): Promise<void> => {
  await connectDB();

  app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
    console.log(`📋 Health check: http://localhost:${PORT}/health`);
  });
};

startServer();
