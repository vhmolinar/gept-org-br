import { test, expect } from '@playwright/test';

const registrationUrl = 'https://autadesouza-online.web.app/#/evento/efas_2026_mg_uberlandia_1';

test.describe('Landing page do EFAS', () => {
  test('exibe as informações essenciais e direciona para a inscrição', async ({ page }) => {
    await page.goto('/efas');

    await expect(page).toHaveTitle('Encontro Fraterno Auta de Souza 2026 | Uberlândia');
    await expect(page.locator('meta[property="og:title"]')).toHaveAttribute('content', 'Encontro Fraterno Auta de Souza 2026 | Uberlândia');
    await expect(page.getByText('Boas vindas ao Grupo Espírita Paulo de Tarso! Uberlândia/MG')).toHaveCount(0);
    await expect(page.getByText(/Inscrições abertas para os Cursos de Espiritismo/)).toHaveCount(0);
    expect(await page.locator('body > header').evaluate((element) => element.getBoundingClientRect().height)).toBeLessThanOrEqual(90);
    await expect(page.getByRole('heading', { level: 1 })).toContainText('Amai-vos uns aos outros');
    await expect(page.getByText('12 e 13 de setembro', { exact: true }).first()).toBeVisible();
    await expect(page.getByText('R$ 20', { exact: true })).toBeVisible();
    await expect(page.getByText('R$ 10', { exact: true })).toBeVisible();
    await expect(page.getByRole('heading', { name: 'Encontrinho', exact: true })).toBeVisible();
    await expect(page.getByRole('heading', { name: 'Cursos oferecidos no EFAS' })).toBeVisible();
    const courseGroups = page.locator('#cursos-efas details');
    const newDimensionsGroup = courseGroups.filter({ hasText: 'Novas Dimensões do Conhecimento' });
    const spiritistCenterGroup = courseGroups.filter({ hasText: 'Temas Vinculados ao Centro Espírita' });

    await newDimensionsGroup.getByText('Ver temas e expositores', { exact: true }).click();
    await expect(page.getByText('Ocultar temas', { exact: true }).first()).toBeVisible();
    await expect(newDimensionsGroup.locator('ol li').first()).toContainText('A arte de contar histórias na Evangelização');
    await expect(newDimensionsGroup.locator('ol li').first()).toContainText('Nite e Hélio Lima');
    await expect(page.getByText('Vencendo a depressão e a culpa em busca da felicidade')).toBeVisible();
    await expect(page.getByText('Lucas Gervásio', { exact: true })).toBeVisible();
    await spiritistCenterGroup.getByText('Ver temas', { exact: true }).click();
    await expect(spiritistCenterGroup.locator('ol li').first()).toContainText('Como evangelizar criança de 0 a 11 anos');
    await expect(spiritistCenterGroup.getByText('A arte de contar histórias na Evangelização')).toHaveCount(0);
    await expect(page.getByText('Geni, Mariana e Lucas Gervásio', { exact: true })).toHaveCount(0);
    await expect(page.getByRole('heading', { name: 'Programação completa' })).toBeVisible();
    await expect(page.getByText('Apresentação artística — show com Moacyr Camargo')).toBeVisible();
    await expect(page.getByText('Almoço de confraternização')).toBeVisible();

    const heroCta = page.getByTestId('efas-hero-cta');
    await expect(heroCta).toHaveAttribute('href', registrationUrl);
    await expect(heroCta).toHaveAttribute('target', '_blank');

    const images = page.locator('main img');
    await expect(images).toHaveCount(10);
    for (const image of await images.all()) {
      await image.scrollIntoViewIfNeeded();
      await expect(image).toBeVisible();
      await expect.poll(() => image.evaluate((element) => element.naturalWidth)).toBeGreaterThan(0);
    }
  });

  test('destaca EFAS no menu e mantém Tratamento Espiritual em Atividades', async ({ page }) => {
    await page.goto('/efas');

    const desktopNav = page.locator('header nav').first();
    await expect(desktopNav.getByRole('link', { name: 'Encontro Fraterno', exact: true })).toBeVisible();
    await expect(desktopNav.getByRole('link', { name: 'Encontro Fraterno', exact: true })).toHaveAttribute('href', '/efas');
    await expect(desktopNav.locator('a[href="/tratamento-espiritual"]')).toHaveText('Tratamento Espiritual');
  });

  test('oferece EFAS e Tratamento Espiritual no menu móvel', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto('/efas');
    await page.getByRole('button', { name: 'Toggle menu' }).click();

    const mobileNav = page.locator('#mobile-menu');
    await expect(mobileNav).toBeVisible();
    await expect(mobileNav.getByRole('link', { name: 'Encontro Fraterno', exact: true })).toBeVisible();
    await expect(mobileNav.getByRole('link', { name: 'Tratamento Espiritual' })).toBeVisible();
  });
});
