/*
 * keeb65 BLE status LED (青 / P1.12)
 *
 * 動作:
 *   アクティブなBTプロファイルが接続された瞬間 -> 点灯
 *   BLE_LED_ON_MS 経過後                      -> 消灯(電池節約)
 *   切断されたら                              -> 即消灯
 * BLE_LED_ON_MS を 0 にすると「接続中はずっと点灯」になる(電池は減りやすい)
 */
#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/led.h>

#include <zmk/event_manager.h>
#include <zmk/events/ble_active_profile_changed.h>
#include <zmk/ble.h>

#define BLE_LED_NODE  DT_NODELABEL(ble_led)
#define BLE_LED_ON_MS 3000

static const struct device *const led_dev = DEVICE_DT_GET(DT_PARENT(BLE_LED_NODE));
static const uint32_t led_idx = DT_NODE_CHILD_IDX(BLE_LED_NODE);

static void ble_led_off_cb(struct k_work *work) {
    ARG_UNUSED(work);
    led_off(led_dev, led_idx);
}
static K_WORK_DELAYABLE_DEFINE(ble_led_off_work, ble_led_off_cb);

static int ble_led_listener(const zmk_event_t *eh) {
    ARG_UNUSED(eh);
    if (!device_is_ready(led_dev)) {
        return ZMK_EV_EVENT_BUBBLE;
    }
    if (zmk_ble_active_profile_is_connected()) {
        led_on(led_dev, led_idx);
        if (BLE_LED_ON_MS > 0) {
            k_work_reschedule(&ble_led_off_work, K_MSEC(BLE_LED_ON_MS));
        }
    } else {
        k_work_cancel_delayable(&ble_led_off_work);
        led_off(led_dev, led_idx);
    }
    return ZMK_EV_EVENT_BUBBLE;
}

ZMK_LISTENER(keeb65_ble_led, ble_led_listener);
ZMK_SUBSCRIPTION(keeb65_ble_led, zmk_ble_active_profile_changed);
