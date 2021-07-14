import { hashSync } from 'bcrypt';
import { Request, Response } from 'express';
import { BlackList, Usuario, Imagen } from '../config/models';
import { TRespuesta } from './dto.response';
import  { compareSync } from 'bcrypt'
import { sign }  from 'jsonwebtoken'
import { RequestCustom } from '../utils/validador';
import { generarUrl } from '../utils/manejoArchivoFirebase'

require("dotenv").config();


export const registro = async ( req: Request, res: Response ):Promise<Response> => {
    try{
        const { email: usuarioCorreo, password: usuarioPassword, nombre: usuarioNombre, tipo: tipoId, imagenId } = req.body;
        const nuevoUsuario = await Usuario.create({usuarioCorreo, usuarioPassword, usuarioNombre, tipoId, imagenId });
        // Solamente el uso de joins (include) funciona en lo que sería los finds
        let respuesta: any = await Usuario.findOne({
            attributes: { exclude: ['usuarioPassword'] },
            where: { usuarioId: nuevoUsuario.getDataValue('usuarioId') },
            include: { model: Imagen },
        });
        const imagen = respuesta?.getDataValue('imagen');
        const url = await generarUrl(imagen.imagenPath, `${imagen.imagenNombre}.${imagen.imagenExtension}`);
        respuesta = { ...respuesta?.toJSON(), url };
        nuevoUsuario.setDataValue('usuarioPassword', null);
        const rpta: TRespuesta = {
            content: respuesta,
            message: "Usuario creado exitosamente",
            success: true,
        }
        return res.status(201).json(rpta);
    }catch(error: any){
        const rpta: TRespuesta = {
            content: error,
            message: "Error al momento de crear al usuario",
            success: false,
        }
        return res.status(400).json(rpta);
    }

    // Metodo 2 
    // const nuevoUsuario = Usuario.build(req.body);
    // const passwordEncriptada = hashSync(req.body.usurioPassword, 10);
    // nuevoUsuario.setDataValue("usurioPassword", passwordEncriptada);
    // nuevoUsuario.save()
}


export const login = async( req: Request, res: Response,  ) => {
    const { email, password }  = req.body;
    const usuario = await Usuario.findOne( {where: { usuarioCorreo: email }} );
    if(usuario){
        console.log(usuario);
        const resultado = compareSync(password, usuario.getDataValue('usuarioPassword'));
        console.log(resultado)
        if(resultado){
            // Si el usuario y la contraseña son las correctas
            const payload = { usuarioId: usuario.getDataValue('usuarioId') };
            const token = sign(payload, String(process.env.JWT_SECRET), { expiresIn: '1h' })
            console.log(token);
            const rpta: TRespuesta = {
                success: true,
                content: token,
                message: `Bienvenido ${usuario.getDataValue('usuarioNombre')}`
            }
            return res.status(400).json(rpta);
        }
    };
    const rpta: TRespuesta = {
        success: false,
        content: null,
        message: 'Credenciales incorrectas'
    }
    return res.status(400).json(rpta);
};

export const perfil = async(req: RequestCustom, res: Response): Promise<Response> => {
    const imagenId = req?.user?.getDataValue('imagenId');
    const imagenEncontrada = await Imagen.findByPk(imagenId);
    const url = await generarUrl( imagenEncontrada?.getDataValue('imagenPath'), `${imagenEncontrada?.getDataValue('imagenNombre')}.${imagenEncontrada?.getDataValue('imagenExtension')}`);
    const content = { ...req?.user?.toJSON(), url }
    const rpta: TRespuesta = {
        content: content,
        message: "",
        success: true
    };
    return res.json(rpta);
}


export const logout = async ( req: Request, res: Response ): Promise<Response> => {
    if(!req.headers.authorization){
        const rpta: TRespuesta = {
            content: null,
            message: 'Error al hacer el logout, se necestia una token en los headers',
            success: false,
        };
        return res.status(400).json(rpta);
    }
    try{
        const token = req.headers.authorization.split(" ")[1];
        await BlackList.create({ blackListToken: token });
        const rpta: TRespuesta = {
            content: null,
            message: 'Usuario Des Logueado',
            success: true,
        }
        // El estado 204 se usa para indicar que la operación ya fue realizada exitosamente  PERO no se retorno nada (no hay contenido)
        return res.status(204).json(rpta);
    }catch(e){
        const rpta: TRespuesta = {
            content: null,
            message: 'El usuario ya fue deslogueado',
            success: false,
        }
        return res.status(400).json(rpta);
    }
}