import express, {Request, Response} from 'express';
import { Express } from 'express';
import { Server as SocketIO } from 'socket.io';
import { createServer, Server as HTTPServer } from 'http';


interface IRegistro {
    username: string;
}

interface IUsuario extends IRegistro{
    id: string,
}

interface IMensaje {
    username: string,
    mensaje: string
    fecha: Date
}

export default class Server {
    app: Express;
    port: string | number;
    httpServer: HTTPServer;
    io: SocketIO;


    constructor(){
        this.app = express();
        this.port = process.env.PORT || 8000;
        this.httpServer = createServer(this.app);
        this.io = new SocketIO(this.httpServer, {cors: {origin: '*'}});
        this.rutas();
        this.escucharSockets();
    }

    rutas(){
        this.app.get('/', (req: Request, res: Response) => {
            res.json({
                success: true,
                message: 'Yo soy la respuesta desde un controlador REST',
            });
        });
    }
    
    escucharSockets(){
        // Se ejecutará cuando el cliente envie ese evento
        // Nosotros podemos crear los eventos que queramos, pero existen métodos ya creados que no se pueden modificar
        let usuarios: IUsuario[] = []
        const mensajes: IMensaje[] = []
        this.io.on('connect', (cliente) => {
            console.log(`Se conectó el cliente ${cliente.id}`);
            cliente.on('registrar', (objCliente: IRegistro) => {
                const usuarioEncontrado = usuarios.filter((usuario)=> usuario.id === cliente.id)[0];
                if(!usuarioEncontrado){
                    usuarios.push({
                        username: objCliente.username,
                        id: cliente.id
                    })
                    console.log(usuarios);
                    this.io.emit('lista-usuarios', usuarios);
                }  
            })

            cliente.on('mensaje-nuevo', (mensaje: string) => {
                const { username } = usuarios.filter((usuario) => usuario.id === cliente.id)[0];
                mensajes.push({
                    mensaje,
                    username,
                    fecha: new Date(),
                });
                this.io.emit('lista-mensajes', mensajes);

                console.log(mensaje)
            })

            cliente.on('disconnect', (razon) => {
                console.log(razon);
                
                usuarios = usuarios.filter((usuario)=>usuario.id !== cliente.id);
                // Estamos haciendo un broadcast estamos enviando el evento a todos los usuarios conectados
                this.io.emit('lista-usuarios', usuarios);
                console.log(`Se desconectó el usuario ${cliente.id}`);
                console.log(usuarios);
            })
            //Si se requiere hacer la emisioon de un evento pero solamente al usuario que la ha solicitado entonces se realizará mediante ese cliente
            cliente.emit('lista-usuarios', usuarios);
            cliente.emit('lista-mensajes', mensajes);
            //Cuando nosotros queremos emitir un evenetoa todos los demas usuarios EXCEPTO al protagonista conectado, entonces haremos un brodcast
            // cliente.broadcast.emit('lista-usuarios', usuarios);
        })
    }

    start(){
        this.httpServer.listen(this.port, ()=>{
            console.log('Servidor corriendo exitosamente');
        });
    }
}