const password = document.getElementById('password')
const btn_enviar = document.getElementById('btn_reset_password')


btn_enviar.addEventListener('click', (evento) => {
    evento.preventDefault
    console.log("Me hizo click");
    const cuerpo = {
        correo: correo.innerText,
        password: password.value
    }
    fetch('http://127.0.0.1:5000/reset-password', {
        method: 'POST',
        body: JSON.stringify(cuerpo),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => {
        // Aca llega todo el bloque de respuesta
        console.log(response.status);
        // El metodo json() retorna una promesa, por lo que es necesario hacer anidamiento de promesas,
        // se retorna dicha promesa y su funcionalidad se dará en el siguiente then que declaremos, no importa cuantas promesas tengamos todas responderan
        // a un solo catch
        return response.json();
    }).then(json => {
        if(json.success){
             Swal.fire({
                 title: "Contraseña cambiada exitosamente",
                 text: json.message,
                 icon: 'success',
                 confirmButtonText: 'Ok'
             }).then((result) => {
                 console.log(result)
                 location.replace(location.origin)
             })
            console.log('Estamos ok')
        } else {    
            console.log(json)
            Swal.fire({
            title: "Error",
            icon: "error",
            text: json.message,
            timer: 2000,
            showConfirmButton: false,
        })}
    }).catch(error => {
        console.log(error)
        Swal.fire({
            title: "Error",
            icon: "error",
            text: "Error de peticion",
            timer: 2000,
            showConfirmButton: false,    
        })
    })
})