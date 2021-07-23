import { Schema, SchemaTypes, model } from 'mongoose';
import { hash, hashSync } from 'bcrypt';


interface Direccion {
    zip?: string,
    calle?: string,
    numero?: number
}

interface Usuario {
    usuarioCorreo: string,
    usuarioNombre: string,
    usuarioApellido: string,
    usuarioTelefono?: string,
    usuarioDni: string,
    usuarioDirreccion?: Direccion,
    usuarioPassword?: string,
    usuarioTipo: string

}

const direccionSchema = new Schema<Direccion>({
    direccionZip: Schema.Types.String,
    dirrecionCalle: Schema.Types.String,
    dirreccionNumero: Schema.Types.Number,
}, { _id: false, timestamps: false });

const usuarioSchema = new Schema<Usuario>({ 
    usuarioCorreo: { type: Schema.Types.String, alias: 'correo', required: true},
    usuarioApellido: { type: Schema.Types.String, alias: 'apellido'},
    usuarioTelefono: { type: Schema.Types.String, alias: 'telefono'},
    usuarioDirreccion: { type: direccionSchema, alias: 'direccion' },
    usuarioDni: { type: Schema.Types.String, alias: 'dni', unique: true, index: true},
    usuarioNombre: { type: Schema.Types.String, alias: 'nombre', required: true, unique: true, index: true },
    usuarioPassword: { type: Schema.Types.String, set: (valor: string) =>  hashSync(valor, 10) , alias: 'password', select: false},
    usuarioTipo: { type: Schema.Types.String, alias: 'tipo', enum: ['CLIENTE', 'PERSONAL']  , required: true }
}, { timestamps: { createdAt: 'fecha_creacion', updatedAt: false } })

export const Usuario = model<Usuario>('usuarios', usuarioSchema);