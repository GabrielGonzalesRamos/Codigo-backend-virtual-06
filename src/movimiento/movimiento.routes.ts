import { Router } from "express";
import { authValidator, personalValidador } from "../utils/validador";
import { crearMovimiento, crearPreferencia, mpEventos } from './movimiento.controllers';

export const movimientoRouter = Router();

movimientoRouter.route('/movimiento').post(authValidator, crearMovimiento);
movimientoRouter.route('/venta').post(authValidator, personalValidador, crearPreferencia);
movimientoRouter.route('/mercadopago-ipn').post(mpEventos);