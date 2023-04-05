const loraPacket = require('lora-packet');
const express = require('express');

const app = express();
app.use(express.json());
app.use(express.static('static'));

app.get('/', function(req, res) {
    res.set('Content-Type', 'text/html');
    res.sendFile('index.html');
});
app.post('/', function(req, res) {
    res.status(400).send("Only GET Request is allowed");
});


/**
 * @description Message Type API
 * @param {object} data                 POST Request body data (json object)
 * @param {string} data.PHYPayload      LoRa PHYPayload (base64 string)
 * 
 * @returns {object} resp               POST Response body data (json object)
 * @returns {string} resp.MessageType   Message Type (UTF-8 string)
 */
app.post('/MessageType', (req, res) => {
    try {

        var data = req.body;
        var MessageType = loraPacket.fromWire(
            Buffer.from(data.PHYPayload, "base64")
        ).getMType().replaceAll(" ", "");
        var resp = {MessageType:MessageType}
        res.setHeader('Content-Type', 'application/json');
        res.send(JSON.stringify(resp));
        
    } catch (error) {
        console.error(error);
        res.status(400).send("Request Parameter Invalid");
    }
});
app.get('/MessageType', (req, res) => {
    res.status(400).send("Only POST Request is allowed");
});


/**
 * @description Join Request API
 * @param {object} data          POST Request body data (json object)
 * @param {string} data.AppKey   Application Key (hex string)
 * @param {string} data.AppEUI   Application EUI (hex string)
 * @param {string} data.DevEUI   Device EUI (hex string)
 * @param {string} data.DevNonce Device Nonce (hex string)
 * 
 * @returns {object} resp               POST Response body data (json object)
 * @returns {string} resp.PHYPayload    LoRa PHYPayload (base64 string)
 */
app.post('/JoinRequest', (req, res) => {
    try {

        var data = req.body;
        if( data.AppKey.length !== 32 ||
            data.DevEUI.length !== 16 || 
            data.AppEUI.length !== 16 || 
            data.DevNonce.length !== 4 )
        {
            throw new Error("Request Parameter Invalid");
        }
        var PHYPayload = loraPacket.fromFields(
            {
                MType: 'Join Request',
                AppEUI: Buffer.from(data.AppEUI, 'hex'),
                DevEUI: Buffer.from(data.DevEUI, 'hex'),
                DevNonce: Buffer.from(data.DevNonce, 'hex')
            }, 
            undefined, undefined,
            AppKey = Buffer.from(data.AppKey, 'hex'),
            undefined, undefined
        ).getPHYPayload()
        var resp = {PHYPayload:PHYPayload.toString('base64'), size:PHYPayload.length}
        res.setHeader('Content-Type', 'application/json');
        res.send(JSON.stringify(resp));
        
    } catch (error) {
        console.error(error);
        res.status(400).send("Request Parameter Invalid");
    }
});
app.get('/JoinRequest', (req, res) => {
    res.status(400).send("Only POST Request is allowed");
});


/**
 * @todo to be implemented only for LoRaWAN V1.1
 * @description Rejoin Request API
 * @param  {object} data          POST Request body data (json object)
 * @param  {string} data.AppKey   Application Key (hex string)
 * @param  {string} data.AppEUI   Application EUI (hex string)
 * @param  {string} data.DevEUI   Device EUI (hex string)
 * @param  {string} data.DevNonce Device Nonce (hex string)
 * 
 * @returns {object} resp               POST Response body data (json object)
 * @returns {string} resp.PHYPayload    LoRa PHYPayload (base64 string)
 */
app.post('/RejoinRequest', (req, res) => {
    res.send("API not implemented")
});
app.get('/RejoinRequest', (req, res) => {
    res.status(400).send("Only POST Request is allowed");
});


/**
 * @description Join Accept API
 * @param {object} data            POST Request body data (json object)
 * @param {string} data.PHYPayload LoRa PHYPayload (base64 string)
 * @param {string} data.AppKey     Application Key (hex string)
 * @param {string} data.DevNonce   Device Nonce : same as JoinRequest (hex string)
 * 
 * @returns {object} resp           POST Response body data (json object)
 * @returns {string} resp.DevAddr   Device Address (hex string)
 * @returns {string} resp.NwkSKey   Network Session Key (hex string)
 * @returns {string} resp.AppSKey   Application Session Key (hex string)
 */
app.post('/JoinAccept', (req, res) => {
    try {
        
        var data = req.body;
        if( data.AppKey.length !== 32 ||
            data.DevNonce.length !== 4 )
        {
            throw new Error("Request Parameter Invalid");
        }
        var packet = loraPacket.fromWire(Buffer.from(data.PHYPayload, 'base64'));
        var decryptedPacket = loraPacket.fromWire(loraPacket.decryptJoinAccept(packet, data.AppKey));
        var keys = loraPacket.generateSessionKeys(
            Buffer.from(data.AppKey, "hex"),
            decryptedPacket.getBuffers().NetID,
            decryptedPacket.getBuffers().AppNonce,
            Buffer.from(data.DevNonce, "hex")
        );
        var resp = {
            DevAddr : decryptedPacket.getBuffers().DevAddr.toString('hex'),
            NwkSKey : keys.NwkSKey.toString('hex'),
            AppSKey : keys.AppSKey.toString('hex'),
        };
        res.setHeader('Content-Type', 'application/json');
        res.send(JSON.stringify(resp));

    } catch (error) {
        console.error(error);
        res.status(400).send("Request Parameter Invalid");
    }
});
app.get('/JoinAccept', (req, res) => {
    res.status(400).send("Only POST Request is allowed");
});


/**
 * @description Unconfirmed Data Up API
 * @param {object} data            POST Request body data (json object)
 * @param {string} data.DevAddr    Device Address (hex string)
 * @param {number} data.FCnt       Frame Counter :  (number from 1 to 65535)
 * @param {number} data.FPort      Frame Port    :  (number from 1 to 255)
 * @param {string} data.payload    payload :  (hex string)
 * @param {string} data.NwkSKey    Network Session Key (hex string)
 * @param {string} data.AppSKey    Application Session Key (hex string)
 * 
 * @returns {object} resp             POST Response body data (json object)
 * @returns {string} resp.PHYPayload  LoRa PHYPayload (base64 string)
 */
app.post('/UnconfirmedDataUp', (req, res) => {
    try {

        var data = req.body;
        if( 
            data.DevAddr.length !== 8  ||
            data.FCnt  < 1  || data.FCnt  > 65535 ||
            data.FPort < 1  || data.FPort > 255   ||
            data.NwkSKey.length !== 32 ||
            data.AppSKey.length !== 32 )
        {
            throw new Error("Request Parameter Invalid");
        }
        var PHYPayload = loraPacket.fromFields(
            {
                MType: 'Unconfirmed Data Up',
                DevAddr: Buffer.from(data.DevAddr, 'hex'),
                FCtrl: {
                    ADR: false,
                    ACK: true,
                    ADRACKReq: false,
                    FPending: false
                },
                FPort : data.FPort,
                FCnt : data.FCnt,
                payload : Buffer.from(data.payload, 'hex')
            },
            Buffer.from(data.AppSKey, 'hex'),
            Buffer.from(data.NwkSKey, 'hex'),
            undefined, undefined, undefined
        ).getPHYPayload();
        var resp = {PHYPayload:PHYPayload.toString('base64'), size:PHYPayload.length}
        res.setHeader('Content-Type', 'application/json');
        res.send(JSON.stringify(resp));		
        
    } catch (error) {
        console.error(error);
        res.status(400).send("Request Parameter Invalid");
    }
});
app.get('/UnconfirmedDataUp', (req, res) => {
    res.status(400).send("Only POST Request is allowed");
});


/**
 * @todo to be implemented
 * @description Unconfirmed Data Down API
 * @param {object} data            POST Request body data (json object)
 * @param {string} data.PHYPayload LoRa PHYPayload (base64 string)
 * @param {string} data.AppKey     Application Key (hex string)
 * @param {string} data.DevNonce   Device Nonce : same as JoinRequest (hex string)
 * 
 * @returns {object} resp           POST Response body data (json object)
 * @returns {string} resp.DevAddr   Device Address (hex string)
 * @returns {string} resp.NwkSKey   Network Session Key (hex string)
 * @returns {string} resp.AppSKey   Application Session Key (hex string)
 */
app.post('/UnconfirmedDataDown', (req, res) => {
    res.send("API not implemented")
});
app.get('/UnconfirmedDataDown', (req, res) => {
    res.status(400).send("Only POST Request is allowed");
});


/**
 * @description Confirmed Data Up API
 * @param {object} data            POST Request body data (json object)
 * @param {string} data.DevAddr    Device Address (hex string)
 * @param {number} data.FCnt       Frame Counter :  (number from 1 to 65535)
 * @param {number} data.FPort      Frame Port    :  (number from 1 to 255)
 * @param {string} data.payload    payload :  (hex string)
 * @param {string} data.NwkSKey    Network Session Key (hex string)
 * @param {string} data.AppSKey    Application Session Key (hex string)
 * 
 * @returns {object} resp             POST Response body data (json object)
 * @returns {string} resp.PHYPayload  LoRa PHYPayload (base64 string)
 */
app.post('/ConfirmedDataUp', (req, res) => {
    try {

        var data = req.body;
        if( 
            data.DevAddr.length !== 8  ||
            data.FCnt  < 1  || data.FCnt  > 65535 ||
            data.FPort < 1  || data.FPort > 255   ||
            data.NwkSKey.length !== 32 ||
            data.AppSKey.length !== 32 )
        {
            throw new Error("Request Parameter Invalid");
        }
        var PHYPayload = loraPacket.fromFields(
            {
                MType: 'Confirmed Data Up',
                DevAddr: Buffer.from(data.DevAddr, 'hex'),
                FCtrl: {
                    ADR: false,
                    ACK: true,
                    ADRACKReq: false,
                    FPending: false
                },
                FCnt: data.FCnt,
                FPort : data.FPort,
                payload : Buffer.from(data.payload, 'hex')
            },
            Buffer.from(data.AppSKey, 'hex'),
            Buffer.from(data.NwkSKey, 'hex'),
            undefined, undefined, undefined
        ).getPHYPayload();
        var resp = {PHYPayload:PHYPayload.toString('base64'), size:PHYPayload.length};
        res.setHeader('Content-Type', 'application/json');
        res.send(JSON.stringify(resp));		
        
    } catch (error) {
        console.error(error);
        res.status(400).send("Request Parameter Invalid");
    }
});
app.get('/ConfirmedDataUp', (req, res) => {
    res.status(400).send("Only POST Request is allowed");
});


/**
 * @todo to be implemented
 * @description Confirmed Data Down API
 * @param {object} data            POST Request body data (json object)
 * @param {string} data.PHYPayload LoRa PHYPayload (base64 string)
 * @param {string} data.AppKey     Application Key (hex string)
 * @param {string} data.DevNonce   Device Nonce : same as JoinRequest (hex string)
 * 
 * @returns {object} resp           POST Response body data (json object)
 * @returns {string} resp.DevAddr   Device Address (hex string)
 * @returns {string} resp.NwkSKey   Network Session Key (hex string)
 * @returns {string} resp.AppSKey   Application Session Key (hex string)
 */
app.post('/ConfirmedDataDown', (req, res) => {
    res.send("API not implemented")
});
app.get('/ConfirmedDataDown', (req, res) => {
    res.status(400).send("Only POST Request is allowed");
});


app.listen(8080, () => console.log(`Started Server on port 8080`));