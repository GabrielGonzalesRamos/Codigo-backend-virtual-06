import { Sequelize, Options } from "sequelize";
require("dotenv").config();

export const opciones : Options = {
    dialect: "postgres",
    timezone: "-05:00",
    logging: false,
    ssl: true, 
    dialectOptions: {
        ssl: true
    }
}

export default new Sequelize( String(process.env.DATABASE_URL), opciones );