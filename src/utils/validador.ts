import { JwtHeader, JwtPayload, verify } from 'jsonwebtoken';
import { NextFunction, Request, Response } from 'express';
import { Usuario } from '../usuario/usuario.model';
require('dotenv').config();


export interface RequestUser extends Request {
    user?: any
}

interface IPayload extends JwtPayload {
    usuarioId?: string
}

const verificarToken = (token: string): IPayload | string  => {
    try {
        const payload = verify(token, String(process.env.JWT_SECRET));
        return payload;
    } catch (error: any) {
        return error.message;
    }
};

export const authValidator = async(req: RequestUser, res: Response, next: NextFunction) => {
    if(!req.headers.authorization){
        return res.status(401).json({
            success: false,
            content: null,
            message: 'Se necesita una token para este request',
        });
    }
    const token = req.headers.authorization.split(' ')[1];
    const resultado = verificarToken(token);

    if(typeof resultado === 'object'){
        const id = resultado.usuarioId;
        const usuario = await Usuario.findById(id, '-usuarioPassword  -__v');
        req.user = usuario
        next()
    } else {
        return res.status(401).json({
            success: false,
            content: resultado,
            message: 'Token invalida'
        })
    }
}


export const personalValidador = (req: RequestUser, res: Response, next: NextFunction) => {
    if(req.user.usuarioTipo === 'PERSONAL'){
        next();
    }else{
        return res.status(401).json({
            success: false,
            content: null,
            message: 'El usuario no dispone de privilegios suficientes'
        });
    };
};