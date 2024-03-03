const express = require('express')

const api = express()

const HOST = 'localhost'
const PORT = 5005

api.get('/test', (req,res) => {
    res.send('Success')
})


api.listen(PORT, () => console.log(`API running at ${HOST}:${PORT}!`))

