const test = require('firebase-functions-test')({
    projectId: 'gept-org-br'
});
const { expect } = require('chai');
const myFunctions = require('../index.js');
const admin = require('firebase-admin');

describe('saveCourseLead', () => {
    after(() => {
        test.cleanup();
    });

    it('should return 405 if method is not POST', async () => {
        const req = { method: 'GET' };
        const res = {
            status: (code) => {
                expect(code).to.equal(405);
                return {
                    json: (data) => {
                        expect(data.error).to.equal('Method Not Allowed. Use POST.');
                    }
                };
            }
        };
        await myFunctions.saveCourseLead(req, res);
    });

    it('should save a valid lead', async () => {
        const req = {
            method: 'POST',
            body: {
                name: 'Test User',
                email: 'test@example.com',
                city: 'Uberlandia',
                state: 'MG',
                whatsapp: '34999999999'
            }
        };
        
        let responseCode = null;
        let responseData = null;
        const res = {
            status: (code) => {
                responseCode = code;
                return {
                    json: (data) => {
                        responseData = data;
                    }
                };
            }
        };
        
        await myFunctions.saveCourseLead(req, res);
        
        expect(responseCode).to.equal(200);
        expect(responseData.success).to.be.true;
        expect(responseData.id).to.exist;

        // Verify it was actually written to Firestore (using emulator)
        const doc = await admin.firestore().collection('course_leads').doc(responseData.id).get();
        expect(doc.exists).to.be.true;
        expect(doc.data().name).to.equal('Test User');
    });
});
