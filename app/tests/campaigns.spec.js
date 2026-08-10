import { test, expect } from '@playwright/test';

test.describe('Gerenciador de Campanhas e Pop-up/Banner', () => {

  test('deve carregar e exibir o pop-up de campanha vigente na Home Page', async ({ page }) => {
    // Acessa a Home Page onde a campanha tipo popup deve ser exibida
    await page.goto('/');

    // Aguarda o pop-up ser exibido
    const popup = page.locator('#promo-popup');
    await expect(popup).toBeVisible({ timeout: 5000 });

    // Verifica o título e elementos do pop-up
    await expect(page.locator('#popup-content')).toBeVisible();
    await expect(page.locator('#popup-content')).toContainText(/conheça o\s*espiritismo/i);

    // Clica no botão de fechar e verifica se oculta
    const closeBtn = page.locator('#popup-close');
    await closeBtn.click();
    await expect(popup).toBeHidden();
  });

  test('não deve exibir o pop-up quando a campanha estiver expirada', async ({ page }) => {
    // Intercepta a requisição do arquivo de campanhas e simula uma campanha expirada
    await page.route('**/data/campaigns.json', async route => {
      await route.fulfill({
        contentType: 'application/json',
        json: {
          campaigns: [
            {
              id: 'campanha-expirada-teste',
              title: 'Campanha Expirada',
              active: true,
              type: 'popup',
              startDate: '2025-01-01T00:00:00-03:00',
              expirationDate: '2025-01-31T23:59:59-03:00',
              targetPages: ['/'],
              content: {}
            }
          ]
        }
      });
    });

    await page.goto('/');

    // Pop-up não deve estar visível
    const popup = page.locator('#promo-popup');
    await expect(popup).toBeHidden();
  });

  test('deve exibir o banner de topo quando houver uma campanha tipo banner ativa', async ({ page }) => {
    // Intercepta e simula uma campanha tipo banner ativa
    await page.route('**/data/campaigns.json', async route => {
      await route.fulfill({
        contentType: 'application/json',
        json: {
          campaigns: [
            {
              id: 'banner-teste',
              title: 'Banner Teste',
              active: true,
              type: 'banner',
              startDate: '2026-01-01T00:00:00-03:00',
              expirationDate: '2026-12-31T23:59:59-03:00',
              targetPages: ['all'],
              content: {
                text: 'Banner de Teste Automatizado Ativo!',
                ctaText: 'Confira',
                ctaLink: '/cursos-espiritismo'
              }
            }
          ]
        }
      });
    });

    await page.goto('/');

    // Verifica que o banner está visível e contém a mensagem esperada
    const banner = page.locator('#campaign-banner');
    await expect(banner).toBeVisible();
    await expect(page.locator('#campaign-banner-text')).toContainText('Banner de Teste Automatizado Ativo!');

    // Fecha o banner e valida ocultação
    await page.click('#campaign-banner-close');
    await expect(banner).toBeHidden();
  });

});
