import { Router } from "express";
import {
  deposit,
  withdraw,
  transfer,
  getTransactions,
} from "../controllers/transaction.controller";
import { protect } from "../middleware/auth.middleware";
import { validate } from "../middleware/validate.middleware";
import {
  depositSchema,
  withdrawSchema,
  transferSchema,
} from "../validators/transaction.validator";

const router = Router();

router.use(protect);

router.post("/deposit", validate(depositSchema), deposit);
router.post("/withdraw", validate(withdrawSchema), withdraw);
router.post("/transfer", validate(transferSchema), transfer);
router.get("/", getTransactions);

export default router;
