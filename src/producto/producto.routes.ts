import { Router } from "express";
import { crearProducto, mostrarProductos, actualizarProducto, eliminarProducto } from './producto.controllers';
import { actualizarProductoDto } from './dto.request'


export const productoRouter = Router();

productoRouter.route('/productos').post(crearProducto).get(mostrarProductos);
productoRouter.route('/productos/:id').patch(actualizarProducto).put(actualizarProductoDto, actualizarProducto).delete(eliminarProducto);