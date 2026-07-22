import { test, expect } from '@playwright/test';

test('should submit the course registration form successfully', async ({ page }) => {
  // Navigate to the courses page
  await page.goto('/cursos-espiritismo');

  // Ensure the form is visible
  await expect(page.locator('#course-form')).toBeVisible();

  // Fill out the form
  await page.fill('#name', 'Playwright Test User');
  await page.fill('#email', 'test@example.com');
  await page.fill('#city', 'Uberlândia');
  await page.selectOption('#state', 'MG');
  await page.fill('#whatsapp', '34999999999');

  // We mock the Firebase function endpoint so we can test the UI logic
  // perfectly without needing the Firebase Emulator to be running alongside it!
  await page.route('**/saveCourseLead', async route => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Return a successful JSON response matching our Firebase function's expected output
    await route.fulfill({ json: { success: true, id: 'mocked-id-123' } });
  });

  // Submit the form
  await page.click('#submit-btn');

  // Expect the button state to change to sending (optional, since it happens fast, but good practice)
  await expect(page.locator('#btn-text')).toHaveText('Enviando...');

  // Expect the success message to appear and have the correct text
  const successMessage = page.locator('#form-message');
  await expect(successMessage).toBeVisible();
  await expect(successMessage).toContainText('Inscrição enviada com sucesso');
  
  // Verify the form resets
  await expect(page.locator('#name')).toHaveValue('');
});
