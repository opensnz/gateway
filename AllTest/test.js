// "use strict";
const loraPacket = require("lora-packet");



// //-----------------
// // packet decoding
const appEUI = '0000000000000000';
const devEUI = '81265ca0e788dfaf';
const appKey = 'ebd350cb50aa25d34e16019469ca3e75';
const gatewayEUI = '5b4931f97b1c0a8e';
// // decode a packet
const packet = loraPacket.fromWire(Buffer.from("IBhmgb/vpx4Q1ecaEFk6G5oUtscZbmXhiMEExu7TNOuQ", "base64"));
const decryptedPacket = loraPacket.fromWire(loraPacket.decryptJoinAccept(packet, appKey));
var keys= loraPacket.generateSessionKeys(
    Buffer.from(appKey, "hex"),
    decryptedPacket.getBuffers().NetID,
    decryptedPacket.getBuffers().AppNonce,
    Buffer.from("C8EA", "hex")
)

// // debug: prints out contents
// // - contents depend on packet type
// // - contents are named based on LoRa spec
console.log("packet.toString()=\n" + packet);
console.log("decryptedPacket.toString()=\n" + decryptedPacket);
console.log("keys=\n" , keys);

// // e.g. retrieve payload elements
// console.log("packet MIC=" + packet.MIC.toString("hex"));
// console.log("FRMPayload=" + packet.FRMPayload.toString("hex"));

// // check MIC
// const NwkSKey = Buffer.from("44024241ed4ce9a68c6a8bc055233fd3", "hex");
// console.log("MIC check=" + (lora_packet.verifyMIC(packet, NwkSKey) ? "OK" : "fail"));

// // calculate MIC based on contents
// console.log("calculated MIC=" + lora_packet.calculateMIC(packet, NwkSKey).toString("hex"));

// // decrypt payload
// const AppSKey = Buffer.from("ec925802ae430ca77fd3dd73cb2cc588", "hex");
// console.log("Decrypted (ASCII)='" + lora_packet.decrypt(packet, AppSKey, NwkSKey).toString() + "'");
// console.log("Decrypted (hex)='0x" + lora_packet.decrypt(packet, AppSKey, NwkSKey).toString("hex") + "'");

// //-----------------
// // packet creation

// // create a packet
// const constructedPacket = lora_packet.fromFields(
//   {
//     MType: "Unconfirmed Data Up", // (default)
//     DevAddr: Buffer.from("01020304", "hex"), // big-endian
//     FCtrl: {
//       ADR: false, // default = false
//       ACK: true, // default = false
//       ADRACKReq: false, // default = false
//       FPending: false, // default = false
//     },
//     FCnt: Buffer.from("0003", "hex"), // can supply a buffer or a number
//     payload: "test",
//   },
//   Buffer.from("ec925802ae430ca77fd3dd73cb2cc588", "hex"), // AppSKey
//   Buffer.from("44024241ed4ce9a68c6a8bc055233fd3", "hex") // NwkSKey
// );
// console.log("constructedPacket.toString()=\n" + constructedPacket);
// const wireFormatPacket = constructedPacket.getPHYPayload();
// console.log("wireFormatPacket.toString()=\n" + wireFormatPacket.toString("hex"));

// const loraPacket = require('lora-packet');
const crypto = require('crypto');// 

// Generate the AppNonce, DevNonce and MIC
const appNonce = crypto.randomBytes(2);




const devNonce = crypto.randomBytes(2);

// const loraPayload = loraPacket.fromFields({
//     MType: 'Join Request',
//     AppEUI: Buffer.from(appEUI, 'hex'),
//     DevEUI: Buffer.from(devEUI, 'hex'),
//     DevNonce: devNonce
//   })
//   console.log("loraPayload", loraPayload)
//const encoded = loraPacket.encrypt(payload);
//console.log(encoded);
const scenario = {
    application: {
        appeui: appEUI,
		appkey: appKey,
    },
    device: {
        deveui: devEUI
    },
    gateway: {
        frequency: 868100000,
        modulation: 'LORA',
        datarate: 'SF8BW125',
        codr: '4/5',
        rssi: -97,
        snr: 12,
    },
}





