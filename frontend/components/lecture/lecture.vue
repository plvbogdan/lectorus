<script setup>
import { marked } from 'marked'

const props = defineProps({
  content: {
    type: Object,
    default: {}
  },
  title: {
    type: String,
    default: ''
  }
})

const sections = computed(() => {
  if (!props.content || !Array.isArray(props.content)) return []
  
  return props.content.map((item, index) => {
    const title = item.title?.[0] || `Раздел ${index + 1}`
    const cleanTitle = title.split(' ').slice(1).join(' ')
    // Создаем безопасный ID для якоря
    const anchorId = `section-${index}-${cleanTitle
      .toLowerCase()
      .replace(/[^a-zа-яё0-9]+/g, '-')
      .replace(/^-|-$/g, '')}`
    
    return {
      id: anchorId,
      title: cleanTitle,
      index
    }
  })
})

// Функция для парсинга markdown
const parseMarkdown = (source) => {
  if (!source) return ''
  
  // Если source - массив строк, объединяем их
  const text = Array.isArray(source) ? source.join('\n') : source
  return marked.parse(text)
}

// Функция для обработки output (ищем изображения)
const processOutput = (source) => {
  if (!source) return { 
    text: '', 
    image: null,
    type: 'unknown'
  }
  
  const result = { 
    text: '', 
    image: null,
    type: 'unknown'
  }
  
  try {
    // Случай 1: Output содержит изображение (как в твоём примере)
    if (source['image/png']) {
      const imageData = source['image/png']
      
      // Проверяем формат base64
      if (typeof imageData === 'string' && imageData.startsWith('iVBORw')) {
        result.image = `data:image/png;base64,${imageData}`
        result.type = 'image'
      }
      
      // Если есть текстовое описание
      if (source['text/plain'] && Array.isArray(source['text/plain'])) {
        result.text = source['text/plain'].join('\n')
      }
    }
    
    // Случай 2: Output содержит только текст
    else if (source['text/plain'] && Array.isArray(source['text/plain'])) {
      result.text = source['text/plain'].join('\n')
      result.type = 'text'
    }
    
    // Случай 3: Если source - просто массив строк (старый формат)
    else if (Array.isArray(source)) {
      result.text = source.join('\n')
      result.type = 'text'
      
      // Проверяем, нет ли base64 изображения в массиве
      source.forEach(item => {
        if (typeof item === 'string' && item.startsWith('iVBORw')) {
          result.image = `data:image/png;base64,${item}`
          result.type = 'image'
        }
      })
    }
    
    // Случай 4: Если source - строка
    else if (typeof source === 'string') {
      result.text = source
      result.type = 'text'
    }
    
  } catch (error) {
    console.error('Ошибка обработки output:', error)
    result.text = 'Ошибка отображения output'
    result.type = 'error'
  }
  
  return result
}

const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId)
  if (element) {
    const offset = 100 // Отступ сверху
    const elementPosition = element.getBoundingClientRect().top
    const offsetPosition = elementPosition + window.pageYOffset - offset
    
    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    })
    
    // Добавляем класс активности для подсветки текущего раздела
    document.querySelectorAll('.lecture-sidebar__link').forEach(link => {
      link.classList.remove('active')
    })
    event.target.classList.add('active')
  }
}
</script>

<template>
  <div class="lecture">
		<aside v-if="sections.length > 0" class="lecture-sidebar">
      <div class="lecture-sidebar__sticky">
        <h3 class="lecture-sidebar__title">Содержание</h3>
        <nav class="lecture-sidebar__nav">
          <ul class="lecture-sidebar__list">
            <li 
              v-for="section in sections" 
              :key="section.id"
              class="lecture-sidebar__item"
            >
              <a 
                :href="`#${section.id}`"
                class="lecture-sidebar__link"
                @click.prevent="scrollToSection(section.id)"
              >
                {{ section.title }}
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </aside>
		<div class="lecture__inner">
			<h1 class="lecture__title" v-html="title"/>
			<div v-for="(item, itemIndex) in content" :key="itemIndex" class="lecture__section" :id="sections[itemIndex]?.id">
				<h2 class="lecture__subtitle" v-html="item.title?.[0].split(' ').slice(1).join(' ')"/>
				
				<div class="lecture__section-inner">
					<div v-for="(cell, cellIndex) in item.content" :key="cellIndex" class="cell">
						<!-- Markdown cell -->
						<div v-if="cell.type === 'markdown'" class="cell-markdown" v-html="parseMarkdown(cell.source)" />
						
						<!-- Code cell -->
						<div v-else-if="cell.type === 'code'" class="cell-code">
							<UiCode
								:source="cell.source"
								language="python"
								:show-line-numbers="true"
							/>
						</div>
						
						<!-- Output cell -->
						<div v-else-if="cell.type === 'output'" class="cell-output" :class="`output-${processOutput(cell.source).type}`">
							
							<!-- Изображение -->
							<div v-if="processOutput(cell.source).image" class="output-image">
								<img 
									:src="processOutput(cell.source).image" 
									:alt="`Output ${itemIndex}-${cellIndex}`"
									@load="console.log('Изображение загружено')"
									@error="console.log('Ошибка загрузки изображения')"
								/>
							</div>
							
							<!-- Текст -->
							<div v-if="processOutput(cell.source).text" class="output-text">
								<pre>{{ processOutput(cell.source).text }}</pre>
							</div>
							
							<!-- Отладка: показываем raw данные если тип unknown -->
							<div v-if="processOutput(cell.source).type === 'unknown'" class="output-debug">
								<details>
									<summary>Raw output data (debug)</summary>
									<pre>{{ JSON.stringify(cell.source, null, 2) }}</pre>
								</details>
							</div>
							
						</div>
						
						<!-- Неизвестный тип ячейки -->
						<div v-else class="cell-unknown">
							<p><strong>Неизвестный тип ячейки:</strong> {{ cell.type }}</p>
							<pre>{{ JSON.stringify(cell, null, 2) }}</pre>
						</div>
					</div>
				</div>
			</div>
		</div>
    
  </div>
</template>

<style src="./__lecture.scss" lang="scss" />