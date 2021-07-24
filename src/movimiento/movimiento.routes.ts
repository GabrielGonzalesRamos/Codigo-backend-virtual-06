import { Router } from "express";
import { authValidator, personalValidador } from "../utils/validador";
import { crearMovimiento, crearPreferencia, mpEventos, listarMovimientos } from './movimiento.controllers';

export const movimientoRouter = Router();

movimientoRouter.route('/movimiento').post(authValidator, crearMovimiento).get(authValidator, listarMovimientos);
movimientoRouter.route('/venta').post(authValidator, personalValidador, crearPreferencia);
movimientoRouter.route('/mercadopago-ipn').post(mpEventos);