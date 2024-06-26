import { NestFactory } from "@nestjs/core"
import { AppModule } from "@src/app.module"
import * as cookieParser from "cookie-parser"
import { ValidationPipe } from "@nestjs/common"

async function bootstrap() {
    const envFile =
        process.env.npm_lifecycle_event === "start:dev" ? "http://localhost:3000" : "https://o-key.anhye0n.com"

    const app = await NestFactory.create(AppModule)

    // console.log(envFile)
    app.enableCors({
        origin: envFile,
        allowedHeaders: ["Content-Type", "Origin", "X-Requested-With", "Accept", "Authorization"],
        exposedHeaders: ["Authorization"],
        credentials: true
    })

    app.useGlobalPipes(
        new ValidationPipe({
            whitelist: true,
            forbidNonWhitelisted: true,
            transform: true
        })
    )
    app.use(cookieParser())

    await app.listen(5005)
}

bootstrap()
