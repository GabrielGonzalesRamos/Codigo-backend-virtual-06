import { Request, Response } from "express";
import { sign } from 'jsonwebtoken'
import { Usuario }  from './usuario.model';
import { compareSync } from 'bcrypt'


export const registro = async(req: Request, res: Response) => {
    console.log(req.body);
    try{
        const nuevoUsuario = await Usuario.create(req.body);
        const data = nuevoUsuario.toJSON()
        delete data['usuarioPassword']
        // delete nuevoUsuario._doc['usuarioPassword']
        // delete nuevoUsuario._doc['_id']
        // delete nuevoUsuario._doc['__v']
        return res.status(201).json({
            success: true,
            content: data,
            message: "Usuario creado exitosamente",
            });
    }catch(error){
        return res.status(400).json({
            success: true,
            content: error,
            message: "error al guardar el usuario",
            });   
    }
    
}

export const login = async(req: Request, res: Response) => {
    const { correo, password } = req.body;
    const usuario = await Usuario.findOne({ usuarioCorreo: correo },/** Indicar que columnas queremos mostrar */ 'usuarioPassword usuarioTipo usuarioNombre');
    console.log(usuario);
    if(!usuario || usuario.usuarioTipo === 'CLIENTE'){
        return res.status(404).json({
            success: false,
            message: 'correo o password incorrectos',
            content: null
        })
    }
    const resultado = compareSync(password, usuario.usuarioPassword ?? '');
    if(resultado){
        // Generar la JWT
        const payload = {
            usuarioId: usuario._id,
            usuarioTipo: usuario.usuarioTipo,
            usuarioNombre: usuario.usuarioNombre,
        }
        const token = sign(payload, process.env.JWT_SECRET ?? '', { expiresIn: '1h' });
        return res.status(200).json({
            success: true,
            content: token,
            message: `Bienvenido ${usuario.usuarioNombre}`,
        });
    }else{
        return res.status(404).json({
            success: false,
            message: 'correo o password incorrectos',
            content: null
        })
    }
};