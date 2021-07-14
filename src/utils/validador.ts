import { verify } from 'jsonwebtoken';
import {  Request, Response, NextFunction } from 'express'
import { TRespuesta } from '../controllers/dto.response';
import { BlackList, Usuario, Tipo } from '../config/models';
import { Model, Op } from 'sequelize';

export interface RequestCustom extends Request {
    user?: Model | null
}


const verificarToken = ( token: string ) => {
    try{
        const payload = verify(token, String(process.env.JWT_SECRET));
        return payload;
    }catch(e: any){
        console.log(e.message);
        return e.message
    }
}

export const authValidator = async(req: RequestCustom, res: Response, next: NextFunction) => {
    if(!req.headers.authorization){
        const rpta: TRespuesta = {
            content: null,
            message: 'Se necesita una token en authorizations',
            success: false,
        };
        return res.status(401).json(rpta);
    }
    const token = req.headers.authorization.split(" ")[1];
    // ['Bear', '12312334564sdfsdfsdfsdf']
    const respuesta = verificarToken(token);
    const blackListToken = await BlackList.findByPk(token);
    console.log(blackListToken);
    // const blackListToken2 = await BlackList.findOne({ where: { blackListToken: token } })
    if(blackListToken){
        const rpta: TRespuesta = {
            content: null,
            message: 'Token invalida',
            success: false
        }
        return res.status(401).json(rpta);
    }
    console.log(respuesta);
    console.log(respuesta.usuarioId);

    if (typeof respuesta === 'object'){
        console.log('Token valido');
        const usuario = await Usuario.findByPk(respuesta.usuarioId, { attributes: { exclude: ['usuarioPassword'] }, logging: true });
        req.user = usuario;
        // console.log(usuario);
        // console.log(usuario?.getDataValue('usuarioNombre')); // Tambien se puede hacer un "if" para consultar si primero existe el usuarioNombre y ya no se
        // Usaría el "?"

        // Buscar ese usuario en la BD según el usuario
    }else{
        const rpta: TRespuesta = {
            content: null,
            message: 'Token invalida',
            success: false,
        };
        return res.status(401).json(rpta);
    }
    next();
}



export const isAdmin = async(req: RequestCustom, res: Response, next: NextFunction) => {
    const administrador = await Tipo.findOne({ where: { tipoDescripcion: { [Op.like]: "%ADMINISTRADOR%" }, tipoId: req.user?.getDataValue('tipoId') } });
    if( administrador ){
        next();
    }else{
        const rpta: TRespuesta = {
            content: null,
            message: 'El usuario no es administrador',
            success: false,
        };
        return res.status(401).json(rpta);
    }
};

