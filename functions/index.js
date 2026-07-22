const { onRequest } = require("firebase-functions/v2/https");
const admin = require("firebase-admin");

admin.initializeApp();
const db = admin.firestore();

exports.saveCourseLead = onRequest({ region: "us-east1", cors: true }, async (req, res) => {
    if (req.method !== "POST") {
        res.status(405).json({ error: "Method Not Allowed. Use POST." });
        return;
    }

    try {
        const { name, email, city, state, whatsapp } = req.body;
        
        if (!name || !email) {
            res.status(400).json({ error: "Name and email are required fields." });
            return;
        }

        const leadData = {
            name,
            email,
            city: city || "",
            state: state || "",
            whatsapp: whatsapp || "",
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        };

        const docRef = await db.collection("course_leads").add(leadData);

        res.status(200).json({ success: true, id: docRef.id });
    } catch (error) {
        console.error("Error saving lead:", error);
        res.status(500).json({ error: "Internal Server Error" });
    }
});
