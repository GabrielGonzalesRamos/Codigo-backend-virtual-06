import { Schema, SchemaTypes, model } from 'mongoose';


interface Detalle {
    detalleCantidad: number,
    detallePrecio: number,
    productoId: string,
}

interface Pasarella {
    pagador?: string,
}

export interface IMovimiento{
    movimientoFecha?: Date,
    movimientoTipo: string,
    usuarioId: string,
    vendedorId: string,
    movimientoDetalles: Array<Detalle>,
    movimientoPasarela?: Pasarella,
}

const detalleSchema = new Schema<Detalle>({
    detalleCantidad: { type: Schema.Types.Number, alias: 'cantidad' },
    detallePrecio: { type: Schema.Types.Decimal128, alias: 'precio', required: true },
    productoId: { type: Schema.Types.ObjectId, alias: "producto_id", required: true,  },
}, { _id: false })

const pasarellaSchema = new Schema<Pasarella>({
    pagador: { type: Schema.Types.String, alias: 'payer' },
}, { _id: false })

const movimientoSchema = new Schema({
    movimientoFecha: { type: Schema.Types.Date, alias: 'fecha', default: new Date()},
    movimientoTipo: { type: Schema.Types.String, alias: 'tipo', enum: ['INGRESO', 'EGRESO'], required: true },
    usuarioId: { type: Schema.Types.ObjectId, alias: 'usuario_id', required: true },
    vendedorId: { type: Schema.Types.ObjectId, alias: 'vendedor_id', required: true },
    movimientoDetalles: { type: [detalleSchema], alias: 'detalles', required: true },
    movimientoPasarela: { type: pasarellaSchema, alias: 'pago' },
});

export const Movimiento = model<IMovimiento>('movimientos', movimientoSchema);