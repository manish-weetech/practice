import Account from '../models/Account';

export const generateAccountNumber = async (): Promise<string> => {
  let accountNumber: string;
  let exists = true;

  do {
    accountNumber = '10' + Math.floor(Math.random() * 1e8).toString().padStart(8, '0');
    exists = !!(await Account.exists({ accountNumber }));
  } while (exists);

  return accountNumber;
};
