import { Request, Response } from 'express';
import { Imagen } from '../config/models';
import { subirArchivo } from '../utils/manejoArchivoFirebase'
import { TRespuesta } from './dto.response';

export const subirImagen = async(req: Request, res: Response) => {
    // /subirImagen?carpeta=usuario
    // /subirImagen?carpeta=producto
    // req.params
    const { carpeta } = req.query;
    console.log(req.query)
    console.log(carpeta)
    if(!carpeta){
        return res.status(400).json({
            message: 'falta carpeta de destino'
        })
    }
    console.log(req.file);  
    if (req.file){
        const archivo = req.file
        try{
            
            // luego de subir el archivo a firebase, guardaremos la imagen
            const nombre = archivo.originalname.split('.');
            const extension = nombre[nombre.length - 1];
            const archivo_sin_extension = archivo.originalname.replace(`.${extension}`, '');
            const nombre_archivo = `${archivo_sin_extension}_${Date.now()}`;
            archivo.originalname = `${nombre_archivo}.${extension}`;
            const link = await subirArchivo(req.file, String(carpeta));

            const nuevaImagen = await Imagen.create({
                imagenNombre: nombre_archivo,
                imagenExtension: extension,
                imagenPath: carpeta
            });
            const content = { ...nuevaImagen.toJSON(), link }
            const rpta: TRespuesta = {
                content,
                message: 'Archivo subido exitosamente',
                success: true,
            }
            return res.status(200).json(rpta);
        }catch(e){
            const rpta: TRespuesta = {
                content: null,
                message: 'Error al crear la imagen',
                success: false,
            }
            return res.status(400).json(rpta);
        }
    }
}