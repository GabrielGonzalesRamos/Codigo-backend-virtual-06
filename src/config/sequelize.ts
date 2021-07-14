import { Sequelize, Options } from "sequelize";
require("dotenv").config();

export const opciones : Options = {
    dialect: "postgres",
    timezone: "-05:00",
    logging: false,
    dialectOptions: process.env.NODE_ENV != 'production'
    ? {} : { ssl: { rejectUnauthorized: false },} ,
}

export default new Sequelize( String(process.env.DATABASE_URL), opciones );