import { Request, Response, NextFunction } from "express";
import { z } from "zod";
import { StatusCodes } from "http-status-codes";

export const validate =
  (schema: z.ZodTypeAny) =>
  (req: Request, res: Response, next: NextFunction): void => {
    const result = schema.safeParse(req.body);

    if (!result.success) {
      const errors = result.error.issues.map((e) => ({
        field: e.path.join("."),
        message: e.message,
      }));

      res.status(StatusCodes.UNPROCESSABLE_ENTITY).json({
        success: false,
        message: "Validation failed",
        errors,
      });
      return;
    }

    req.body = result.data;
    next();
  };
