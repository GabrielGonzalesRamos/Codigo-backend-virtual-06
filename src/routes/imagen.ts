import { Router, Request, Response, NextFunction } from 'express';
import Multer from 'multer';
import { subirImagen, eliminarArchivoUtil } from '../controllers/imagen';

const multer = Multer({
    storage: Multer.memoryStorage(),
    // limits: {
    //     // fileSize tamaño máximo del archivo, expresado en bytes
    //     fileSize: 5 * 1024 * 1024
    // }
});
export const imagenRouter = Router();

imagenRouter.post('/subirImagen', multer.single('imagen'), (req: Request, res: Response, next: NextFunction) => {
    const archivo = req.file;
    if(archivo?.size && archivo?.size > 5242880 ){
        return res.status(400).json({message: 'Archivo demasiado grande'});
    }else{
        next();
    }
} ,subirImagen);




imagenRouter.delete('/eliminarImagen', eliminarArchivoUtil);