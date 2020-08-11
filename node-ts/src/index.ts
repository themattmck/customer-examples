import tracer from './tracer'
import express, {Request, Response} from 'express';

const app = express();

app.get('/async', async (req: Request, res: Response) => {
    return await tracer.trace('insideAsyncRoute', async () => {
        const x = await listIsvs()
        console.log(x)
        res.send({"route":"/example"})
    })
});

app.get("/example", async (req: Request, res: Response, next) => {
        tracer.trace('req.getBasic', span => {
        })
        res.send({"Hello":"World"})
    }

);

app.listen(3000,() => {
    console.log("Running on 3000")
})


async function listIsvs(): Promise<string> {
    return await tracer.trace('async.trace', async (span) => {
        span?.addTags({"Key":"value"})
        return new Promise<string>((resolve, reject) => {
            setTimeout(function() {
                resolve('hello world');
            }, 2000);
        })
    })
}
