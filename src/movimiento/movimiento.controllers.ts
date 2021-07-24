import { Request, Response } from "express";
import { Producto } from "../producto/producto.model";
import { RequestUser } from "../utils/validador";
import { IMovimiento, Movimiento } from './movimiento.model'
import { configure, preferences } from 'mercadopago'
import { CreatePreferencePayload, PreferenceItem } from "mercadopago/models/preferences/create-payload.model";
import { Usuario } from "../usuario/usuario.model";
import { isTemplateSpan } from "typescript";
import fetch from "node-fetch";
require('dotenv').config();

//interface IMovimiento extends Omit<Movimiento, 'vendedorId' | 'usuarioId' | 'movimientoDetalles'> {}
interface Movimiento extends Omit<IMovimiento, 'vendedorId'> {}



export const crearMovimiento = async(req: RequestUser, res: Response) => {
    const vendedor = req.user._id
    const { movimientoFecha, movimientoTipo, movimientoDetalles, usuarioId }: IMovimiento = req.body;
    try{
        const usuario = await Usuario.findById(usuarioId);
        if(!usuario){
            return res.json({
                success: true,
                content: null,
                message: 'El usuario no existe',
            });   
        }
        await Promise.all(
            movimientoDetalles.map(async(detalle) => {
                console.log(detalle.productoId);
                console.log(detalle.detalleCantidad);
                const producto = await Producto.findById(detalle.productoId);
                if(!producto){
                    throw new Error(`No existe el producto con el id ${detalle.productoId}`)
                }
                detalle.detallePrecio = Number(producto?.productoPrecio);
                console.log(Number(producto?.productoPrecio))
                console.log(producto);
            })
        );
        const movimiento : IMovimiento = {
         movimientoFecha,
         movimientoTipo,
         movimientoDetalles,
         usuarioId,
         vendedorId: vendedor
     };
       const nuevoMovimiento = await Movimiento.create(movimiento);
        console.log('final');
        return res.json({
            success: true,
            content: movimiento,
            message: 'Movimiento registrado exitomsante',
        });
    }catch(error: any){
        return res.status(400).json({
            success: false,
            content: error.message,
            message: 'Error al crear el movimiento',
        });
    }
};


export const crearPreferencia = async(req: Request, res: Response) => {
    // Solamente un personal puede crear una preferencia 
    // De acuerdo al ID del movimiento por el body buscar en la BD si existe sino no proceder
    // Devolver todos los detalles con sus respectivos productos
    configure({
        access_token: String(process.env.ACCESS_TOKEN_MP),
        integrator_id: String(process.env.INTEGRATOR_ID_MP)
    })
    console.log(String(process.env.ACCESS_TOKEN_MP))
    console.log(String(process.env.INTEGRATOR_ID_MP))
    const payload: any = {
        auto_return: "approved",
        notification_url: process.env.NOTIFICATION_URL,
        back_urls: {
          success: process.env.SUCCESS_URL,
          failure: process.env.FAILURE_URL,
          pending: process.env.PENDING_URL },
        payment_methods: {
            excluded_payment_methods: [
                {
                    id: "master"
                },
                {
                    id: "debvisa"
                }
            ],
            installments: 5 } };
        // items: [
        //   {
        //     id: "123123",
        //     title: "zapatito de bebe",
        //     description: "Zapato de moda primavera otoño 2021",
        //     picture_url: "http://imagen.com",
        //     category_id: "1",
        //     quantity: 1,
        //     currency_id: "PEN",
        //     unit_price: 40.8,
        //   },
        // ],
        // payer: {
        //   name: "Eduardo",
        //   surname: "De Rivero",
        //   email: "test_user_46542185@testuser.com",
        //   phone: {
        //     area_code: "51",
        //     number: 974207075,
        //   },
        //   identification: {
        //     type: "DNI",
        //     number: "22334445",
        //   },
        //   address: {
        //     zip_code: "04002",
        //     street_name: "Av Primavera",
        //     street_number: 1150,
        //   },
        //   date_created: "2021-07-21",
        // },


    console.log(req.body)
    const { movimientoId } = req.body;
    try {
    //   const preferencia = await preferences.create(payload);
    //   console.log(preferencia);
      const movimiento = await Movimiento.findById(movimientoId);
      if (!movimiento) {
        throw new Error();
      }
      const usuario = await Usuario.findById(movimiento.usuarioId)
      console.log(usuario);
      if(!usuario){
        throw new Error('Usuario no encontrado');
      }
      payload.payer = {
          name: usuario.usuarioNombre,
          surname: usuario.usuarioApellido,
          address: { 
              zip_code: usuario.usuarioDirreccion?.zip ?? '',
              street_name: usuario.usuarioDirreccion?.calle ?? '',
              street_number: usuario.usuarioDirreccion?.numero ?? 0,
          },
          phone: {
              area_code: '51',
              number: usuario.usuarioTelefono ? +usuario.usuarioTelefono : 0,
          },
          email: 'test_user_46542185@testuser.com',
          identification: {
              type: 'DNI',
              number: usuario.usuarioDni
          }
           
      }
      const items: PreferenceItem[] = []
      console.log()
      await Promise.all(
        movimiento.movimientoDetalles.map( async(detalle) => {
            const producto = await Producto.findById(detalle.productoId);
            if(producto){
                const x: PreferenceItem = {
                    id: detalle.productoId,
                    title: producto?.productoNombre,
                    description: '',
                    picture_url: req.get('host')+'/'+producto?.productoImagen,
                    category_id: producto?.productoTipo,
                    quantity: detalle.detalleCantidad,
                    currency_id: 'PEN',
                    unit_price: Number(detalle.detallePrecio),
                };
                items.push(x);
                console.log(x);
            }
        } )
      );
      payload.items = items;
      const preferencia = await preferences.create(payload);


      //console.log(movimiento);
      // devolver todos los detalles con sus  respectivos productos
      // {
      //   movimientoId: "123123l2313k13j";
      // }
      return res.json({
        success: true,
        content: preferencia.response.init_point,
        message: 'Compra exitosa'
      });
    } catch (error: any) {
      console.log(error)
      return res.status(404).json({
        success: false,
        content: error.message,
        message: `El movimiento no existe`,
      });
    }
  };


  export const mpEventos = async(req: Request, res: Response) => {
      const { id, topic } = req.query
      console.log('BODY:-------------------------------------------');
      console.log(req.body);
      console.log('QUERY:-------------------------------------------');
      if(topic === 'payment'){
        const response = await fetch(
            `https://api.mercadopago.com/v1/payments/${id}`,
            { headers: { Authorization: process.env.ACCESS_TOKEN_MP ?? '' } }
        )
        const json = await response.json();
        console.log('------------ESTO ES UN PAGO----------------------')
        console.log(id)
        console.log(json)
        console.log(json.status);
        console.log('------------ESTO ES UN PAGO----------------------')
        console.log('-------------------------------------------');
      }
      console.log(req.query);
      return res.status(200).json({});
  };