import express, {  Request, Response, Express, NextFunction } from "express";
import { json } from "body-parser"
import conexion from "./sequelize"
import { tipoRouter } from "../routes/tipo"
import { accionRouter } from "../routes/accion"
import morgan from 'morgan'
import { usuarioRouter } from "../routes/usuario";
import { productoRouter } from "../routes/producto";
import { imagenRouter } from '../routes/imagen'
import { movimientoRouter } from "../routes/movimiento";
import documentacion from './swagger.json';
import swaggerUI from 'swagger-ui-express'

require('dotenv').config();


export default class Server{
    app: Express;
    port: string = "";
    constructor(){
        this.app = express();
        this.port = process.env.PORT || "8000";
        this.bodyParser();
        this.CORS();
        this.rutas();
    }
    bodyParser(){
        this.app.use(json());
        this.app.use(morgan('common'));
    }
    CORS(){
        this.app.use((req: Request, res: Response, next: NextFunction) => {
            // Sirve para indicar que origenes o dominios pueden acceder a mi API
            res.header('Access-Control-Allow-Origin', process.env.DOMINIOS);
            // Indica que tipos de cabecera pueden ser enviadas
            res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
            // Indica que metodos pueden intentar acceder a mi backend
            res.header('Acces-Control-Allow-Methods', 'GET,POST,PUT,DELETE');
            // Si es que cumple el origen, el header y el metodo entonces daremos paso al controlador solicitado
            next();
            
        })
    }
    rutas(){
        this.app.get('/', (req: Request, res: Response) => {
            res.send('Bienvenido a la API de zapatería');
        });
        process.env.NODE_ENV != 'production' ? ( documentacion.host = `127.0.0.1:${this.port}`, documentacion.schemes = ['http'] ) : ( documentacion.host = `zapateria-ts-ggonzales.herokuapp.com`, documentacion.schemes = ['https'] );
        this.app.use('/docs', swaggerUI.serve, swaggerUI.setup(documentacion));
        this.app.use(tipoRouter);
        this.app.use(accionRouter);
        this.app.use(usuarioRouter);
        this.app.use(productoRouter);
        this.app.use(imagenRouter);
        this.app.use(movimientoRouter);
    }
    start(){
        this.app.listen(this.port, async() => {
            console.log("Servidor corriendo exitosamente");
            try{
                await conexion.sync();
                console.log('Base de datos sincronizada');
            }catch(error){
                console.error(error)
            }
        });
    };
}

// { force: true }