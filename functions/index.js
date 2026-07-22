const { onRequest } = require("firebase-functions/v2/https");
const { defineSecret } = require('firebase-functions/params');
const admin = require("firebase-admin");
const { getFirestore } = require("firebase-admin/firestore");

const whatsappVerifyToken = defineSecret('WHATSAPP_VERIFY_TOKEN');
admin.initializeApp();
const db = getFirestore(admin.app(), "gept-org-br");

exports.saveCourseLead = onRequest({ region: "us-east1", cors: true }, async (req, res) => {
    if (req.method !== "POST") {
        res.status(405).json({ error: "Method Not Allowed. Use POST." });
        return;
    }

    try {
        const { name, email, city, state, whatsapp } = req.body;

        // Backend Validation
        if (!name || typeof name !== 'string' || name.trim().length < 3) {
            return res.status(400).json({ error: "Nome inválido ou muito curto." });
        }
        if (!email || !/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email)) {
            return res.status(400).json({ error: "E-mail inválido." });
        }
        if (!city || typeof city !== 'string') {
            return res.status(400).json({ error: "Cidade é obrigatória." });
        }
        if (!state || state.length !== 2) {
            return res.status(400).json({ error: "Estado inválido." });
        }
        if (!whatsapp || whatsapp.replace(/\D/g, '').length < 10) {
            return res.status(400).json({ error: "WhatsApp inválido. Inclua o DDD." });
        }

        const docRef = await db.collection("course_leads").add({
            name: name.trim(),
            email: email.trim().toLowerCase(),
            city: city.trim(),
            state: state.toUpperCase(),
            whatsapp: whatsapp.replace(/\D/g, ''), // Save only digits
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });

        res.status(200).json({ success: true, id: docRef.id });
    } catch (error) {
        console.error("Error saving lead:", error);
        res.status(500).json({ error: "Internal Server Error" });
    }
});

exports.saveCampaignLeads = onRequest({ region: "us-east1", cors: true }, async (req, res) => {
    if (req.method !== "POST") {
        res.status(405).json({ error: "Method Not Allowed. Use POST." });
        return;
    }

    try {
        const { name, email, city, state, whatsapp, type } = req.body;

        // Backend Validation
        if (!name || typeof name !== 'string' || name.trim().length < 3) {
            return res.status(400).json({ error: "Nome inválido ou muito curto." });
        }
        if (!email || !/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email)) {
            return res.status(400).json({ error: "E-mail inválido." });
        }
        if (!city || typeof city !== 'string') {
            return res.status(400).json({ error: "Cidade é obrigatória." });
        }
        if (!state || state.length !== 2) {
            return res.status(400).json({ error: "Estado inválido." });
        }
        if (!whatsapp || whatsapp.replace(/\D/g, '').length < 10) {
            return res.status(400).json({ error: "WhatsApp inválido. Inclua o DDD." });
        }
        
        const validTypes = ["AUTA_DE_SOUZA", "CHICO_XAVIER", "MADRE_TEREZA", "EVANGELIZACAO_INFANTIL"];
        if (!type || !validTypes.includes(type)) {
            return res.status(400).json({ error: "Tipo de campanha inválido." });
        }

        const docRef = await db.collection("campaign_leads").add({
            name: name.trim(),
            email: email.trim().toLowerCase(),
            city: city.trim(),
            state: state.toUpperCase(),
            whatsapp: whatsapp.replace(/\D/g, ''), // Save only digits
            type: type,
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });

        res.status(200).json({ success: true, id: docRef.id });
    } catch (error) {
        console.error("Error saving campaign lead:", error);
        res.status(500).json({ error: "Internal Server Error" });
    }
});

exports.saveContactMessage = onRequest({ region: "us-east1", cors: true }, async (req, res) => {
    if (req.method !== "POST") {
        res.status(405).json({ error: "Method Not Allowed. Use POST." });
        return;
    }

    try {
        const { name, reply_preference, whatsapp, email, message } = req.body;

        if (!name || typeof name !== 'string' || name.trim().length < 3) {
            return res.status(400).json({ error: "Nome inválido ou muito curto." });
        }
        
        if (reply_preference !== "WhatsApp" && reply_preference !== "Email") {
            return res.status(400).json({ error: "Preferência de resposta inválida." });
        }

        if (reply_preference === "WhatsApp") {
            if (!whatsapp || whatsapp.replace(/\D/g, '').length < 10) {
                return res.status(400).json({ error: "WhatsApp inválido. Inclua o DDD." });
            }
        }

        if (reply_preference === "Email") {
            if (!email || !/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email)) {
                return res.status(400).json({ error: "E-mail inválido." });
            }
        }

        if (!message || typeof message !== 'string' || message.trim().length < 5) {
            return res.status(400).json({ error: "Sua mensagem é muito curta." });
        }

        const docRef = await db.collection("contato").add({
            name: name.trim(),
            reply_preference: reply_preference,
            whatsapp: whatsapp ? whatsapp.replace(/\D/g, '') : null,
            email: email ? email.trim().toLowerCase() : null,
            message: message.trim(),
            status: "NOVO",
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });

        res.status(200).json({ success: true, id: docRef.id });
    } catch (error) {
        console.error("Error saving contact message:", error);
        res.status(500).json({ error: "Internal Server Error" });
    }
});

// WhatsApp Business API Webhook
exports.whatsappWebhook = onRequest({ region: "us-east1", secrets: [whatsappVerifyToken] }, (req, res) => {
    if (req.method === "GET") {
        // This token must match the one you configure in the Meta App Dashboard
        const VERIFY_TOKEN = whatsappVerifyToken.value();
        
        const mode = req.query["hub.mode"];
        const token = req.query["hub.verify_token"];
        const challenge = req.query["hub.challenge"];

        if (mode && token) {
            if (mode === "subscribe" && token === VERIFY_TOKEN) {
                console.log("WhatsApp Webhook verified!");
                res.status(200).send(challenge);
            } else {
                console.warn("WhatsApp Webhook verification failed. Token mismatch.");
                res.sendStatus(403);
            }
        } else {
            res.sendStatus(400);
        }
    } else if (req.method === "POST") {
        // Handle incoming WhatsApp messages/status updates here in the future
        const body = req.body;
        console.log("Incoming WhatsApp Webhook:", JSON.stringify(body, null, 2));
        res.sendStatus(200);
    } else {
        res.status(405).send("Method Not Allowed");
    }
});
