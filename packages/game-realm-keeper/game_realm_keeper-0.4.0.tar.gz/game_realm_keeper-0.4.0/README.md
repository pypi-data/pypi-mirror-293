# This is a RPG resources management toolkit that allows you to create and manage your own RPG game.

## 架構

### 1. GameObject
- **描述**：最基本的遊戲物件類別，代表遊戲中的角色、物品等。
- **屬性**：
  - id：物件唯一標識符
  - type：物件類型（如角色、物品）
  - attributes：物件屬性字典
  - equipment：裝備物品字典

### 2. GameWorld
- **描述**：代表整個遊戲世界的狀態。
- **功能**：
  - 管理多個 GameObject 實例
  - 管理遊戲規則
  - 提供添加、獲取、更新和刪除遊戲物件的方法

### 3. GameManager
- **描述**：管理單個遊戲實例的核心邏輯。
- **功能**：
  - 使用 GameWorld 維護遊戲狀態
  - 通過 GameRepository 保存和載入遊戲狀態
  - 提供高級操作：
    - 創建角色和物品
    - 設置物件屬性
    - 裝備物品

### 4. GameRepository（抽象類別）
- **描述**：定義遊戲狀態持久化的介面。
- **功能**：
  - 保存遊戲狀態
  - 載入遊戲狀態
  - 刪除遊戲狀態

### 5. GameSessionManager
- **描述**：管理多個遊戲會話。
- **功能**：
  - 創建新遊戲
  - 獲取現有遊戲
  - 結束遊戲會話
  - 刪除遊戲數據

## 具體實現

### MemoryGameRepository
- **描述**：GameRepository 的記憶體實現。
- **功能**：
  - 在記憶體中存儲和檢索遊戲數據

## 類別關係

1. **GameObject** ⇒ **GameWorld**
   - GameWorld 管理多個 GameObject 實例

2. **GameWorld** ⇒ **GameManager**
   - GameManager 使用 GameWorld 來維護遊戲狀態

3. **GameManager** ⇒ **GameRepository**
   - GameManager 通過 GameRepository 保存和載入遊戲狀態

4. **GameSessionManager** ⇒ **GameManager**
   - GameSessionManager 創建和管理多個 GameManager 實例

5. **GameSessionManager** ⇒ **GameRepository**
   - GameSessionManager 使用 GameRepository 來初始化 GameManager

## 職責劃分

1. **數據層**：GameRepository
   - 負責遊戲數據的持久化操作

2. **邏輯層**：GameManager
   - 處理單個遊戲實例的邏輯

3. **應用層**：GameSessionManager
   - 管理遊戲會話，協調多個遊戲實例

4. **模型層**：GameObject 和 GameWorld
   - 定義遊戲的基本結構和狀態

## Todo

- 也需要幫 GameManager 加一個 service 層，如果遊戲邏輯變得複雜，可以考慮在 GameWorld 和 GameInterface 之間引入 Service
  層，這一層可以處理更具體的領域邏輯，如戰鬥系統、庫存管理等
