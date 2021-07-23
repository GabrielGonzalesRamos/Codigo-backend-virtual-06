import { Request, Response, NextFunction } from "express";



export type TActualizarProducto = {
    productoNombre: string;
    productoPrecio: number;
    productoImagen: string;
    productoTipo: string;
};

export const actualizarProductoDto = ( req: Request, res: Response, next: NextFunction ) => {
    const data: TActualizarProducto = req.body;
    const tipos = [ 'LATTES',  'COMIDA', 'MERCHANDISING', 'FRAPPS'];
    const resultadoTipo = tipos.filter((tipo) => tipo === data.productoTipo[0])
    console.log(resultadoTipo)
    if ( data.productoNombre && data.productoImagen && data.productoPrecio && resultadoTipo ){
        next();
    }else {
        const rpta = {
            success: false,
            content: null,
            message: 'Falta campos',
        } 
        return res.status(400).json(rpta);
    }
}