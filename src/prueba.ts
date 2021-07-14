let nombre: string = "eduardo";

enum ESexo {
  MASCULINO = "MASCULINO",
  FEMENINO = "FEMENINO",
}


// 
interface IPersona {
    nombre: string,
    edad: number,
    sexo ?: ESexo
}

type TPersona = {
  nombre: string;
  edad: number;
  sexo?: ESexo;
};

let persona: TPersona = {
  edad: 18,
  nombre: "raul",
  sexo: ESexo.FEMENINO,
};

function prueba<T>(personas: T[]): T {
  return personas[0];
}

function prueba2(personas: any[]): any {
  return personas[0];
}

let respersona = prueba(["eduardo", "jose", "ricardo"]);
const edades = prueba([18, 20, 30, 50]);
edades.toExponential();

// const nota = prueba2([1, 2, 3]);
const nota = prueba2(['eduardo','paul']);
console.log(nota.toExponential());
prueba([1, 2, 3]);
prueba(["raul", "carlos", "daniel", "ricardo"]);
prueba([true, false, "true"]);

console.log(typeof nota)