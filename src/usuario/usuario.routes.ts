import { Router } from "express";
import { registro, login } from './usuario.controller';
import { registroDto } from './dto.request';

export const usuarioRouter = Router();

usuarioRouter.route('/registro').post(registroDto, registro);
usuarioRouter.route('/login').post(login);