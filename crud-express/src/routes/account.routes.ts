import { Router } from "express";
import {
  getMyAccounts,
  getAccountById,
  toggleAccountStatus,
} from "../controllers/account.controller";
import { protect } from "../middleware/auth.middleware";

const router = Router();

router.use(protect);

router.get("/", getMyAccounts);
router.get("/:id", getAccountById);
router.patch("/:id/toggle", toggleAccountStatus);

export default router;
