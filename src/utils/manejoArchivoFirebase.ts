import { Storage } from '@google-cloud/storage';
require('dotenv').config()
//  Primero creo la instancia de la clase Storage con la configuración
// de las credenciales y el id del proyecto
const storage = new Storage({ 
    projectId: 'zapateria-codigo-gabriel',  
    credentials: {
        client_email: process.env.CLIENT_EMAIL_FIREBASE,
        private_key: process.env.PRIVATE_KEY_FIREBASE?.replace(/\\n/gm, '\n')
    }
});

// Enlazo mi bucket ( Donde se almancenará todas las imagenes)
// Se copia el link que muestra el bucket PERO sin el protocolo gs ni el "/" del final
const bucket = storage.bucket('zapateria-codigo-gabriel.appspot.com')

export const subirArchivo = (archivo: Express.Multer.File, path: string): Promise<string> => {

    return new Promise(( resolve, reject ) => {
        if(!archivo){
            reject('No se encontró el archivo');
        }
        // Aquí comienza el proceso de subida de imagen
        const newFile = bucket.file(`${path}/${archivo.originalname}`);
        // Agregar configuración adicional de nuestro archivo como su metada
        const blobStream = newFile.createWriteStream({ metadata: { contentType: archivo.mimetype }})
        // Ahora puedo realizar eventos
        blobStream.on('error', (e)=> {
            reject(e.message);
        })
        // Veremos el evento si es que la carga termino exitosamente
        blobStream.on('finish', async()=>{
            try{
                // La fecha actual + 1000 ms  * segundos * minutos
                const link = await newFile.getSignedUrl({ action: 'read', expires: Date.now() + 1000 * 1 * 60  }) //MM-DD-YYYY // Esto retornará un link
                return resolve(link.toString());
            }catch(e){
                reject(e);
            }
        });
        blobStream.end(archivo.buffer);
    })
};

export const generarUrl = async (carpeta: string, filename: string): Promise<String> => {
    try{
        const url = await bucket.file(`${carpeta}/${filename}`).getSignedUrl({ action: 'read', expires: Date.now() + 1000 * 1 * 60 });
        return url.toString();
    }catch(e: any){
        return e;
    }
}

export const eliminarArchivoUtil = async(carpeta: string, archivo: string) => {
    try{
        const respuesta = await bucket.file(`${carpeta}/${archivo}`).delete({ignoreNotFound: true});
        console.log(respuesta);
        return respuesta
    }catch(e){
        return e
    }
}