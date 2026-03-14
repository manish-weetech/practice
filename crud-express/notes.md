# 📚 Banking System — Express.js + TypeScript + MongoDB + JWT + Zod

> Complete step-by-step guide. Read this once and you can recreate the project from scratch.

---

## 🗂️ Final Project Structure

```
crud-express/
├── .env
├── .env.example
├── .gitignore
├── tsconfig.json
├── package.json
├── notes.md
└── src/
    ├── server.ts                    ← Entry point
    ├── app.ts                       ← Express app setup (no global errorHandler)
    ├── types/
    │   └── express.d.ts             ← Augments req.user type globally
    ├── config/
    │   ├── db.ts                    ← MongoDB connection (uses dotenv directly)
    │   └── env.ts                   ← Validated env exports
    ├── models/                      ← Pure schemas only, no methods
    │   ├── User.ts                  ← IUser interface + schema
    │   ├── Account.ts               ← IAccount interface + schema
    │   └── Transaction.ts           ← ITransaction + union types
    ├── validators/                  ← Zod schemas (single source of truth)
    │   ├── auth.validator.ts
    │   └── transaction.validator.ts
    ├── middleware/
    │   ├── validate.middleware.ts   ← Generic Zod handler
    │   ├── auth.middleware.ts       ← JWT → req.user
    │   └── error.middleware.ts      ← Simple fallback (not used in app.ts)
    ├── utils/
    │   ├── account.util.ts          ← generateAccountNumber()
    │   └── jwt.util.ts              ← signToken / verifyToken
    ├── controllers/                 ← Business logic + inline res.json()
    │   ├── auth.controller.ts
    │   ├── account.controller.ts
    │   └── transaction.controller.ts
    └── routes/
        ├── auth.routes.ts
        ├── account.routes.ts
        └── transaction.routes.ts
```

---

## 🚀 Step 1 — Prerequisites

- **Node.js** >= 18.x (`node -v`)
- **npm** >= 9.x (`npm -v`)
- **MongoDB Replica Set or Atlas** (required for transactions)

### Start a local Replica Set (one-time)

```bash
# Terminal 1
mongod --replSet rs0 --dbpath /data/db --port 27017

# Terminal 2
mongosh --eval "rs.initiate()"
```

---

## 🚀 Step 2 — Init Project

```bash
mkdir crud-express && cd crud-express
npm init -y
```

---

## 🚀 Step 3 — Install Dependencies

```bash
# Production
npm install express mongoose jsonwebtoken bcryptjs dotenv zod http-status-codes cors

# Dev
npm install --save-dev typescript ts-node-dev @types/node @types/express @types/bcryptjs @types/jsonwebtoken @types/cors
```

| Package | Purpose |
|---|---|
| `express` | HTTP server & routing |
| `mongoose` | MongoDB ODM (built-in TS support) |
| `jsonwebtoken` | JWT sign & verify |
| `bcryptjs` | Password hashing |
| `dotenv` | Load `.env` |
| `zod` | Schema validation (runtime + types) |
| `http-status-codes` | Named status code constants |
| `cors` | CORS headers |
| `typescript` | TypeScript compiler |
| `ts-node-dev` | Dev server with auto-restart |
| `@types/*` | Type definitions for JS packages |

---

## 🚀 Step 4 — Create Config Files

### `tsconfig.json`
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "typeRoots": ["./node_modules/@types", "./src/types"]
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### `.env`
```env
PORT=3000
MONGO_URI=mongodb://localhost:27017/banking_db?replicaSet=rs0
JWT_SECRET=your_super_secret_key_change_this
JWT_EXPIRES_IN=7d
```

### `.gitignore`
```
node_modules/
.env
dist/
*.log
```

### `package.json` scripts
```json
"scripts": {
  "dev":   "ts-node-dev --respawn --transpile-only src/server.ts",
  "build": "tsc",
  "start": "node dist/server.js"
}
```

---

## 🚀 Step 5 — Create Folder Structure

```bash
mkdir -p src/types src/config src/models src/validators src/middleware src/utils src/controllers src/routes
```

---

## 🚀 Step 6 — Create Files (in this order)

### 1. `src/types/express.d.ts`
Extends Express `Request` to include `req.user` **globally** across the entire project.
Without this file, TypeScript would error on `req.user` in every controller.
```ts
import { IUser } from '../models/User';
declare global {
  namespace Express {
    interface Request { user?: IUser; }
  }
}
```

### 2. `src/config/env.ts`
Validates required env vars at startup and exports typed constants.
```ts
import 'dotenv/config';

const _required = (key: string): string => {
  const val = process.env[key];
  if (!val) throw new Error(`Missing required env variable: ${key}`);
  return val;
};

export const PORT          = Number(process.env.PORT) || 3000;
export const MONGO_URI     = _required('MONGO_URI');
export const JWT_SECRET    = _required('JWT_SECRET');
export const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN ?? '7d';
```

### 3. `src/config/db.ts`
Loads dotenv directly and reads `MONGO_URI` from `process.env`.
```ts
import 'dotenv/config';
import mongoose from 'mongoose';

const MONGO_URI = process.env.MONGO_URI as string;

const connectDB = async (): Promise<void> => {
  try {
    const conn = await mongoose.connect(MONGO_URI);
    console.log(`✅ MongoDB Connected: ${conn.connection.host}`);
  } catch (error) {
    console.error(`❌ MongoDB Connection Error: ${(error as Error).message}`);
    process.exit(1);
  }
};

mongoose.connection.on('disconnected', () => console.warn('⚠️  MongoDB disconnected'));
mongoose.connection.on('reconnected',  () => console.log('🔄 MongoDB reconnected'));

export default connectDB;
```

### 4. `src/models/User.ts`
- Interface `IUser extends Document`
- Schema with `select: false` on password
- **No pre-save hook** — password hashing is done in the controller

### 5. `src/models/Account.ts`
- Interface `IAccount extends Document`
- Pure schema: userId, accountNumber (unique), balance, currency, isActive

### 6. `src/models/Transaction.ts`
- Union types: `TransactionType`, `TransactionStatus`
- Interface `ITransaction extends Document`
- Uses `satisfies` keyword to keep enum arrays type-safe

### 7. `src/utils/account.util.ts`
```ts
export const generateAccountNumber = async (): Promise<string> => {
  let accountNumber: string;
  let exists = true;
  do {
    accountNumber = '10' + Math.floor(Math.random() * 1e8).toString().padStart(8, '0');
    exists = !!(await Account.exists({ accountNumber }));
  } while (exists);
  return accountNumber;
};
```

### 8. `src/utils/jwt.util.ts`
`signToken(payload)` and `verifyToken(token)` — thin wrappers around jsonwebtoken.

### 9. `src/validators/auth.validator.ts`
> ⚠️ Zod v4: pass error messages as `{ message: '...' }` object, not a plain string.
```ts
import { z } from 'zod';

export const registerSchema = z.object({
  name:     z.string().trim().min(2, 'Name must be at least 2 characters').max(60),
  email:    z.string().email({ message: 'Invalid email address' }).toLowerCase(),
  password: z.string().min(6, 'Password must be at least 6 characters').max(100),
});

export const loginSchema = z.object({
  email:    z.string().email({ message: 'Invalid email address' }),
  password: z.string().min(1, 'Password is required'),
});

export type RegisterInput = z.infer<typeof registerSchema>;
export type LoginInput    = z.infer<typeof loginSchema>;
```

### 10. `src/validators/transaction.validator.ts`
Zod schemas and inferred types for `deposit`, `withdraw`, `transfer`.

### 11. `src/middleware/validate.middleware.ts`
> ⚠️ Zod v4: use `z.ZodTypeAny` instead of the deprecated `ZodSchema` named import.
```ts
import { z } from 'zod';

export const validate = (schema: z.ZodTypeAny) => (req, res, next): void => {
  const result = schema.safeParse(req.body);
  if (!result.success) {
    const errors = result.error.issues.map(e => ({ field: e.path.join('.'), message: e.message }));
    res.status(422).json({ success: false, message: 'Validation failed', errors });
    return;
  }
  req.body = result.data; // replaced with clean, parsed data
  next();
};
```
Key points:
- Uses `safeParse` — **never throws**
- Replaces `req.body` with the parsed output (unknown fields stripped)
- Controller never touches validation

### 12. `src/middleware/auth.middleware.ts`
Verifies Bearer token → sets `req.user`. Handles `TokenExpiredError` and `JsonWebTokenError` with instanceof checks (not string comparison).

### 13. `src/middleware/error.middleware.ts`
Simple fallback — kept minimal for POC. **Not mounted in `app.ts`**.
Errors are handled directly in each controller with inline `res.status().json()`.
```ts
export const errorHandler = (err: Error, _req, res, _next): void => {
  console.error('[ERROR]', err.message);
  res.status(500).json({ success: false, message: err.message || 'Internal Server Error' });
};
```

### 14–16. Controllers (`auth`, `account`, `transaction`)

All controllers respond **directly** with `res.status().json()` — no response helper utility.
Errors are caught in each `try/catch` and returned inline.

#### Key pattern — password hashing in controller, NOT model:
```ts
const hashedPassword = await bcrypt.hash(password, 12);
const user = await User.create({ name, email, password: hashedPassword });
```
Why: password hashing is **business logic**, not a data concern. Models should only define shape.

#### Key pattern — Zod types on req.body:
```ts
const { email, password } = req.body as LoginInput; // type-safe, no unknown
```

#### Key pattern — inline responses (no helper utility):
```ts
// Success
res.status(200).json({ success: true, message: 'Login successful', data: { token, user } });

// Error
res.status(409).json({ success: false, message: 'Email already registered.' });

// Catch block
res.status(500).json({ success: false, message: (err as Error).message });
```

### 17–19. Routes
```ts
// Clean, declarative — nothing else
router.post('/register', validate(registerSchema), register);
router.post('/login',    validate(loginSchema),    login);
router.get('/me',        protect,                  getMe);
```

### 20. `src/app.ts`
```ts
const app = express();
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use('/api/auth',         authRoutes);
app.use('/api/accounts',     accountRoutes);
app.use('/api/transactions', transactionRoutes);

// 404 handler
app.use((req, res) => {
  res.status(404).json({ success: false, message: `Route ${req.method} ${req.originalUrl} not found` });
});

export default app;
// Note: no app.use(errorHandler) — errors handled per-controller
```

### 21. `src/server.ts`
`server.ts` calls `connectDB()` first, then `app.listen()`.

---

## 🚀 Step 7 — Run

```bash
npm run dev    # development (ts-node-dev)
npm run build  # compile to dist/
npm start      # run compiled output
```

Expected:
```
✅ MongoDB Connected: localhost
🚀 Server running on http://localhost:3000
```

---

## 🏗️ Architecture Principles

### Models = Pure Schemas
```ts
// ✅ Schema only
const userSchema = new Schema<IUser>({ email: String, password: String });

// ❌ Never do this
userSchema.methods.comparePassword = () => {};
userSchema.pre('save', async function() { this.password = hash(...) });
```
Business logic (hashing, generation) lives in **utils** and **controllers**.

### Validation = 3-Layer Separation
```
validators/    → Zod schema          (what shape)
middleware/    → validate(schema)    (how to reject)
controllers/   → business logic      (never sees raw req.body)
```

### Routes = Declarative Chains
```ts
router.post('/deposit', validate(depositSchema), deposit);
//                       ↑ shape check           ↑ business logic
```

### Type Safety on req.body
```ts
// Zod inferred type → no casting guesswork
const { accountId, amount } = req.body as DepositInput;
```

### No Global Error Handler (POC)
Each controller handles its own errors inline. This is simpler for a POC:
```ts
} catch (err) {
  res.status(500).json({ success: false, message: (err as Error).message });
}
```
For production, consider mounting a global `errorHandler` in `app.ts`.

---

## 💳 MongoDB Transaction Pattern

```ts
const session = await mongoose.startSession();
session.startTransaction();
try {
  await account.save({ session });
  await Transaction.create([{ ... }], { session });
  await session.commitTransaction();   // ← atomic commit
} catch (err) {
  await session.abortTransaction();    // ← all writes rolled back
  res.status(500).json({ success: false, message: (err as Error).message });
} finally {
  session.endSession();                // ← always clean up
}
```

---

## 🛣️ API Reference

### Auth `/api/auth`
| Method | Route | Auth | Body |
|---|---|---|---|
| POST | `/register` | ❌ | `{ name, email, password }` |
| POST | `/login` | ❌ | `{ email, password }` |
| GET | `/me` | ✅ | — |

### Accounts `/api/accounts`
| Method | Route | Auth |
|---|---|---|
| GET | `/` | ✅ |
| GET | `/:id` | ✅ |
| PATCH | `/:id/toggle` | ✅ |

### Transactions `/api/transactions`
| Method | Route | Auth | Body |
|---|---|---|---|
| POST | `/deposit` | ✅ | `{ accountId, amount, description? }` |
| POST | `/withdraw` | ✅ | `{ accountId, amount, description? }` |
| POST | `/transfer` | ✅ | `{ fromAccountId, toAccountId, amount, description? }` |
| GET | `/` | ✅ | — |

---

## 🧪 curl Tests

```bash
# Register
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@test.com","password":"secret123"}'

# Login — copy token
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@test.com","password":"secret123"}'

# Deposit
curl -X POST http://localhost:3000/api/transactions/deposit \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"accountId":"<ID>","amount":5000}'

# Transfer (atomic)
curl -X POST http://localhost:3000/api/transactions/transfer \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"fromAccountId":"<ID1>","toAccountId":"<ID2>","amount":1000}'
```

---

## 🔒 Production Checklist

- [ ] Strong random `JWT_SECRET` (64+ chars)
- [ ] Short JWT expiry + refresh token strategy
- [ ] Rate limiting (`express-rate-limit`)
- [ ] Helmet.js (`npm install helmet`) for security headers
- [ ] HTTPS only in production
- [ ] Mount global `errorHandler` in `app.ts` for centralised error logging
- [ ] Store secrets in a secrets manager (not `.env` files)
