import { DataTypes } from "sequelize";
import { hashSync } from 'bcrypt';
import conexion from "./sequelize";


const productoModel =  () => conexion.define("producto", {
    productoId: {
        primaryKey: true,
        type: DataTypes.INTEGER,
        autoIncrement: true,
        unique: true,
        field: 'id'
    },
    productoNombre: {
        type: DataTypes.STRING(35),
        allowNull: false,
        field: 'nombre'
    },
    productoPrecio: {
        type: DataTypes.DECIMAL(5,2),
        field: 'precio',
        allowNull: false,
        validate: {
            isFloat: true,
            validacionPersonalizada(valor: Number){
                if(valor < 0){
                    throw new Error('El precio no puede ser negativo')
                }
            }
        }
    },
    productoEstado: {
        type: DataTypes.BOOLEAN,
        defaultValue: true,
        field: 'estado',
    },
    productoDescripcion: {
        type: DataTypes.STRING(60),
        field: 'descripcion',
    }}, {
        tableName: 'productos',
        timestamps: false,
    });

    
const tipoModel = () => conexion.define('tipo', {
    tipoId: {
        type: DataTypes.INTEGER,
        field: 'id',
        primaryKey: true,
        unique: true,
        autoIncrement: true,
    },
    tipoDescripcion: {
        type: DataTypes.STRING(45),
        field: 'descripcion',
        unique: true,
    },
}, {
    tableName: 'tipos',
    timestamps: false
});

const accionModel = () => conexion.define('accion', {
    accionId: {
        type: DataTypes.INTEGER,
        field: 'id',
        primaryKey: true,
        unique: true,
        autoIncrement: true,
    },
    accionDescripcion: {
        type: DataTypes.STRING(45),
        field: 'descripcion'
    },
}, {
    tableName: 'acciones',
    timestamps: false
});

const usuarioModel = () => conexion.define('usuario', {
    usuarioId: {
        type: DataTypes.INTEGER,
        field: 'id',
        primaryKey: true,
        unique: true,
        autoIncrement: true,  
        allowNull: false,      
    },
    usuarioNombre: {
        type: DataTypes.STRING(50),
        field: 'nombre',
        validate: { 
            is: /([A-Z])\w+([ ])/
        },
        allowNull: false
    },
    usuarioCorreo: {
        type: DataTypes.STRING(35),
        field: 'correo',
        unique: true,
        validate: {
            isEmail: true,
        },
        allowNull: false,
    },
    usuarioPassword: {
        type: DataTypes.TEXT,
        field: 'password',
        allowNull: false,
        set(valor){
            // Encriptando la contraseña
            const passwordEncriptada = hashSync(String(valor), 10);
            console.log(passwordEncriptada);
            this.setDataValue('usuarioPassword', passwordEncriptada)
        }
    },
}, {
    tableName: 'usuarios',
    timestamps: false
})

const movimientoModel = () =>
  conexion.define(
    "movimiento",
    {
      movimientoId: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        unique: true,
        field: "id",
        allowNull: false,
        autoIncrement: true,
      },
      movimientoFecha: {
        type: DataTypes.DATE,
        defaultValue: new Date(),
        field: "fecha",
        allowNull: false,
      },
      movimientoTipo: {
        field: "tipo",
        type: DataTypes.STRING(20),
        // validacion que solamente sea INGRESO | EGRESO
        validate: {
          isIn: [["INGRESO", "EGRESO"]],
        },
        allowNull: false,
      },
      movimientoTotal: {
        type: DataTypes.DECIMAL(5, 2),
        field: "total",
        allowNull: false,
      },
    },
    {
      tableName: "movimientos",
      timestamps: false,
    }
  );
const detalleMovimientoModel = () =>
  conexion.define(
    "detalleMovimiento",
    {
      detalleMovimientoId: {
        field: "id",
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true,
        allowNull: false,
      },
      detalleMovimientoCantidad: {
        field: "cantidad",
        type: DataTypes.INTEGER,
        allowNull: false,
      },
      detalleMovimientoPrecio: {
        field: "precio",
        type: DataTypes.DECIMAL(7, 2),
      },
    },
    {
      tableName: "detalle_movimientos",
      timestamps: false,
    }
  );



const  blackListModel = () => conexion.define('authUser', {
        blackListToken: {
            type: DataTypes.TEXT,
            allowNull: false,
            primaryKey: true,
        }
    },{
        tableName: "auth_user",
        timestamps: false,
    })

const imagenModel = () => conexion.define('imagen', {
    imagenId: {
        primaryKey: true,
        autoIncrement: true,
        type: DataTypes.INTEGER,
        unique: true,
    },
    imagenNombre: {
        type: DataTypes.TEXT,
        allowNull: false,
        field: 'nombre',
    },
    imagenExtension: {
        type: DataTypes.STRING(5),
    },
    imagenPath: {
        type: DataTypes.TEXT,
        field: 'path',
        allowNull: false,
    }},{
        tableName: 'imagenes',
        timestamps: false,
    }
);    
// RELACIONES 

export const Producto = productoModel();
export const Tipo = tipoModel();
export const Accion = accionModel();
export const Usuario = usuarioModel();
export const Movimiento = movimientoModel();
export const DetalleMovimiento = detalleMovimientoModel();
export const BlackList = blackListModel();
export const Imagen = imagenModel();
//BlackList.sync({force: true});

Producto.hasMany(DetalleMovimiento, {foreignKey: { field: 'producto_id', allowNull: false, name: 'productoId' }});
DetalleMovimiento.belongsTo(Producto, { foreignKey: { field: 'producto_id', allowNull: false, name: 'productoId' } });

Tipo.hasMany(Accion, { foreignKey: { field: 'tipo_id',allowNull: false, name: 'tipoId' } });
Accion.belongsTo(Tipo, { foreignKey: { field: 'tipo_id' ,allowNull: false, name: 'tipoId' } });

Tipo.hasMany(Usuario, { foreignKey: { field: 'tipo_id', allowNull: false, name: 'tipoId' } });
Usuario.belongsTo(Usuario, { foreignKey: { field: 'tipo_id', allowNull: false, name: 'tipoId' } });

Usuario.hasMany(Movimiento, { foreignKey: { field: 'usuario_id',  allowNull: false, name: 'usuarioId' } });
Movimiento.belongsTo(Usuario, { foreignKey: { field: 'usuario_id', allowNull: false, name: 'usuarioId' } });

Movimiento.hasMany(DetalleMovimiento, { foreignKey: { field: 'movimiento_id', allowNull: false, name: 'movimientoId' } });
DetalleMovimiento.belongsTo(Movimiento, { foreignKey: { field: 'movimiento_id', allowNull: false , name: 'movimientoId' } });

// Relacion de uno a uno
Imagen.hasOne(Usuario, { foreignKey: { name: "imagenId", field: "imagen_id" },});
Usuario.belongsTo(Imagen, { foreignKey: { name: "imagenId", field: "imagen_id" },});
  
// Relacion de muchos a muchos
Producto.belongsToMany(Imagen, { through: "productos_imagenes" });
Imagen.belongsToMany(Producto, { through: "productos_imagenes" });