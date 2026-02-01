declare global {
    interface Window {
        Telegram?: {
            WebApp?: {
                ready(): void;
                colorScheme?: 'light' | 'dark';
                themeParams?: {
                    bg_color?: string;
                    text_color?: string;
                    hint_color?: string;
                    link_color?: string;
                    button_color?: string;
                    button_text_color?: string;
                    secondary_bg_color?: string;
                };
                openLink?(url: string): void;
                initData?: string;
                initDataUnsafe?: {
                    query_id?: string;
                    user?: {
                        id: number;
                        is_bot?: boolean;
                        first_name: string;
                        last_name?: string;
                        username?: string;
                        language_code?: string;
                        photo_url?: string;
                    };
                    receiver?: {
                        id: number;
                        is_bot: boolean;
                        first_name: string;
                        last_name?: string;
                        username?: string;
                        language_code?: string;
                    };
                    chat?: {
                        id: number;
                        type: string;
                        title?: string;
                        username?: string;
                        photo?: {
                            small_file_id: string;
                            small_file_unique_id: string;
                            big_file_id: string;
                            big_file_unique_id: string;
                        };
                    };
                    auth_date?: number;
                    hash?: string;
                    start_param?: string;
                    can_send_after?: number;
                };
            };
        };
    }
}

export { };